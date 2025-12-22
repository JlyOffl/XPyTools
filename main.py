import threading
import logging
import random
import time
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks

from rest_utils import *  # keep using your existing sync functions/utilities

# ============================
# ADDED: import the bot service
# ============================
from tg_link_bot import TelegramLinkBotService


# ============================================================
# === Config ===
# ============================================================
DEBUG_MODE = False  # Set to False in production

# ============================
# ADDED: Telegram bot config
# ============================
BOT_TOKEN = "8572400565:AAGZfqW9BzdTbpH1_1tVQBRGOcBG1RkZ_iY"
API_ID = 23222227
API_HASH = "285928aad99d749c835f42b631bdc5be"

# MUST be a USER Telethon session (phone login)
TELETHON_SESSION = "tg_user_session_user"


# ============================================================
# === Logging Setup ===
# ============================================================
log_level = logging.DEBUG if DEBUG_MODE else logging.ERROR
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================================
# === FastAPI App ===
# ============================================================
app = FastAPI()

# ============================
# ADDED: initialize bot service
# ============================
tg_bot_service = TelegramLinkBotService(
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    telethon_session=TELETHON_SESSION,
    debug=DEBUG_MODE
)

# === Run-state guard to prevent overlapping /spaces runs ===
_RUNNING_BULK = threading.Event()


# ============================================================
# === FastAPI lifecycle hooks (ADDED)
# ============================================================
@app.on_event("startup")
async def startup_event():
    # Start Telegram link bot in background
    await tg_bot_service.start()


@app.on_event("shutdown")
async def shutdown_event():
    # Stop Telegram link bot cleanly
    await tg_bot_service.stop()


# ============================================================
# === Helpers
# ============================================================
def _clean_username(username: str) -> str:
    return (username or "").strip().lstrip("@")


# ============================================================
# === DRY helpers (reuse across both flows)
# ============================================================
def _fetch_user_space_core(uname: str):
    res = get_user_info_by_screen_name(uname)
    if res is None or not getattr(res, "text", ""):
        DBProxy().DeleteFollower(uname)
        return None

    if not extract_value_from_json_path(res.text, "data"):
        DBProxy().DeleteFollower(uname)
        return None

    rest_id = extract_value_from_json_path(res.text, "rest_id")
    display_name = extract_value_from_json_path(res.text, "name") or uname
    if not rest_id:
        return None

    res = get_space_by_host_id(rest_id)
    DBProxy().UpdateFollowerDisplayName(uname, display_name)

    users_blob = extract_value_from_json_path(res.text, "users")
    if users_blob in (None, "{}", "[]"):
        return None

    space_id = extract_value_from_json_path(res.text, "broadcast_id")
    if not space_id:
        return None

    title = extract_value_from_json_path(res.text, "title") or f"{display_name} Space"
    return rest_id, display_name, space_id, title


def _fetch_audio_core(space_id: str):
    res = get_space_audio_by_id(space_id)
    if res is None or not getattr(res, "text", ""):
        return None

    media_key = extract_value_from_json_path(res.text, "media_key")
    if not media_key:
        return None

    res = get_space_audio_link(media_key)
    if res is None or not getattr(res, "text", ""):
        return None

    audio_url = extract_value_from_json_path(res.text, "noRedirectPlaybackUrl")
    if not audio_url:
        return None

    short_url = shorten_url(audio_url)
    return audio_url, short_url


# ============================================================
# === Main functions (reused in bulk + single)
# ============================================================
def get_audio_space_link(username: str):
    try:
        uname = _clean_username(username)
        if not uname:
            return

        core = _fetch_user_space_core(uname)
        if not core:
            return
        rest_id, user_name, space_id, title = core

        audio_core = _fetch_audio_core(space_id)
        if not audio_core:
            return
        audio_url, short_url = audio_core

        tweet = (
            f"Topic: {title}\n"
            f"ID: https://x.com/{uname} ({user_name})\n"
            f"AudioLink: {short_url}\n"
            f"Space: https://x.com/i/spaces/{space_id}"
        )

        try:
            threading.Thread(
                target=lambda: send_telegram_message(tweet),
                daemon=True
            ).start()
        except Exception as et:
            logger.warning(f"Telegram schedule failed for {uname}: {et}")

    except Exception as e:
        logger.error(f"Error in get_audio_space_link for user {username}: {e}", exc_info=True)


def get_space_info_and_notify(username: str, notify_telegram: bool = True) -> Optional[dict]:
    try:
        uname = _clean_username(username)
        if not uname:
            return None

        core = _fetch_user_space_core(uname)
        if not core:
            return None
        _, user_name, space_id, title = core

        audio_core = _fetch_audio_core(space_id)
        if not audio_core:
            return None
        audio_url, short_url = audio_core

        tweet = (
            f"Topic: {title}\n"
            f"ID: https://x.com/{uname} ({user_name})\n"
            f"AudioLink: {short_url}\n"
            f"Space: https://x.com/i/spaces/{space_id}"
        )

        notified = False
        if notify_telegram:
            try:
                threading.Thread(
                    target=lambda: send_telegram_message(tweet),
                    daemon=True
                ).start()
                notified = True
            except Exception as et:
                logger.warning(f"Telegram schedule failed for {uname}: {et}")

        return {
            "username": uname,
            "display_name": user_name,
            "space_id": space_id,
            "title": title,
            "audio_url": audio_url,
            "short_url": short_url,
            "tweet": tweet,
            "notified": notified
        }

    except Exception as e:
        logger.error(f"get_space_info_and_notify error for {username}: {e}", exc_info=True)
        return None


# ============================================================
# === Adaptive, overlap-safe bulk worker
# ============================================================
def _bulk_spaces_worker(usernames, max_workers: int = 100, delay_range=None):
    from concurrent.futures import ThreadPoolExecutor
    import math

    if _RUNNING_BULK.is_set():
        logger.info("Bulk worker invoked while already running; skipping.")
        return

    _RUNNING_BULK.set()
    try:
        n = len(usernames) if usernames else 0
        if n == 0:
            return

        effective_workers = min(max(10, math.ceil(n / 3)), int(max_workers), n)
        if delay_range is None:
            if n >= 200:
                delay_range = (0.10, 0.30)
            elif n >= 50:
                delay_range = (0.30, 0.80)
            else:
                delay_range = (0.50, 1.50)

        with ThreadPoolExecutor(max_workers=effective_workers) as executor:
            for uname in usernames:
                executor.submit(get_audio_space_link, uname)
                time.sleep(random.uniform(*delay_range))

    finally:
        _RUNNING_BULK.clear()


# ============================================================
# === HTTP Endpoints
# ============================================================
@app.get("/spaces/{username}")
def get_space_for_user(username: str):
    if not username or not username.strip():
        raise HTTPException(status_code=400, detail="Username is required.")

    info = get_space_info_and_notify(username, notify_telegram=True)
    if not info:
        return {
            "status": "No space/audio found",
            "username": _clean_username(username),
            "notified": False
        }

    return {
        "status": "Success",
        **{k: info[k] for k in ("username", "display_name", "space_id", "title", "short_url", "notified")}
    }


@app.get("/spaces")
def fetch_space(background_tasks: BackgroundTasks):
    if _RUNNING_BULK.is_set():
        return {"status": "Already running", "in_progress": True}

    uList = DBProxy().GetFollowingList()
    random.shuffle(uList)
    count = len(uList)

    start_delay = random.uniform(0.0, 5.0)

    def delayed_start():
        time.sleep(start_delay)
        _bulk_spaces_worker(uList, max_workers=100)

    background_tasks.add_task(delayed_start)

    return {"status": "Triggered", "count": count, "jitter_seconds": round(start_delay, 2)}
