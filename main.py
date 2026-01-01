import threading
import logging
import random
import time
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException, BackgroundTasks

from rest_utils import *  # keep using your existing sync functions/utilities


# ============================================================
# === Config ===
# ============================================================
DEBUG_MODE = False  # Set to False in production


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

# === Run-state guard to prevent overlapping /spaces runs ===
_RUNNING_BULK = threading.Event()


# ============================================================
# === Helpers
# ============================================================
def _clean_username(username: str) -> str:
    return (username or "").strip().lstrip("@")


# ============================================================
# === DRY helpers (reuse across both flows)
# ============================================================
def _fetch_user_space_core(uname: str):
    """
    Resolve user -> rest_id -> active space (space_id, title), update DB display name.
    Returns (rest_id, display_name, space_id, title) or None if anything missing.
    Side-effects: DeleteFollower on missing users, UpdateFollowerDisplayName when known.
    """
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
    """
    Resolve media_key -> audio_url -> short_url for a given space_id.
    Returns (audio_url, short_url) or None if anything missing.
    """
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
# === Message builder (used by bulk + single)
# ============================================================
def build_space_message(username: str) -> Optional[str]:
    """
    Build the Discord/Telegram message text for a single username.
    Returns message string or None.
    """
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
        _, short_url = audio_core

        msg = (
            f"Topic: {title}\n"
            f"ID: https://x.com/{uname} ({user_name})\n"
            f"AudioLink: {short_url}\n"
            f"Space: https://x.com/i/spaces/{space_id}"
        )
        return msg

    except Exception as e:
        logger.error(f"build_space_message error for {username}: {e}", exc_info=True)
        return None


# ============================================================
# === Main functions (reused in bulk + single)
# ============================================================
def get_audio_space_link(username: str):
    """
    (Legacy single-thread function) Attempts to find and post a space link for the user.
    NOTE: Bulk flow no longer uses this; bulk consolidates into ONE Discord message.
    """
    try:
        msg = build_space_message(username)
        if not msg:
            return

        # non-blocking notification
        threading.Thread(
            target=lambda: send_discord_message(msg),
            daemon=True
        ).start()

    except Exception as e:
        logger.error(f"Error in get_audio_space_link for user {username}: {e}", exc_info=True)


def get_space_info_and_notify(username: str, notify_telegram: bool = True) -> Optional[dict]:
    """
    Looks up the user's current Space, builds audio link + short URL,
    optionally sends a Telegram message (non-blocking), and returns a dict.
    """
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
            threading.Thread(
                target=lambda: send_telegram_message(tweet),
                daemon=True
            ).start()
            notified = True

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
# === Adaptive, overlap-safe bulk worker (ONE Discord message)
# ============================================================
def _bulk_spaces_worker(usernames, max_workers: int = 100, delay_range=None):
    """
    Builds messages for each username concurrently and sends ONE consolidated Discord message.
    - No message-id storage needed
    - Adds separators between sections
    - If content exceeds Discord 2000-char limit, it will TRUNCATE and report omitted count
      (strict one-message mode).
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import math

    if _RUNNING_BULK.is_set():
        logger.info("Bulk worker already running; skipping.")
        return

    _RUNNING_BULK.set()
    try:
        n = len(usernames) if usernames else 0
        if n == 0:
            return

        effective_workers = min(max(10, math.ceil(n / 3)), max_workers, n)

        if delay_range is None:
            delay_range = (0.1, 0.3) if n >= 200 else (0.3, 0.8) if n >= 50 else (0.5, 1.5)

        results: List[str] = []

        with ThreadPoolExecutor(max_workers=effective_workers) as executor:
            futures = []
            for uname in usernames:
                futures.append(executor.submit(build_space_message, uname))
                time.sleep(random.uniform(*delay_range))

            for f in as_completed(futures):
                try:
                    msg = f.result()
                    if msg:
                        results.append(msg)
                except Exception as e:
                    logger.error(f"Bulk future error: {e}", exc_info=True)

        # Sort (optional) for stable output. You can remove if you prefer arrival order.
        results.sort()

        ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        header = f"🕒 Refresh: {ts}\nCount: {len(results)}\n"

        # Send exactly ONE message (truncate if too long)
        send_discord_message_batch(
            results,
            header=header,
            strict_one_message=False
        )

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
        return {"status": "No space/audio found", "username": _clean_username(username)}

    return {
        "status": "Success",
        **{k: info[k] for k in ("username", "display_name", "space_id", "title", "short_url", "notified")}
    }


@app.get("/spaces")
def fetch_space(background_tasks: BackgroundTasks):
    if _RUNNING_BULK.is_set():
        return {"status": "Already running", "in_progress": True}

    ulist = DBProxy().GetFollowingList()
    random.shuffle(ulist)

    delay = random.uniform(0, 5)

    background_tasks.add_task(
        lambda: (time.sleep(delay), _bulk_spaces_worker(ulist))
    )

    return {
        "status": "Triggered",
        "count": len(ulist),
        "jitter_seconds": round(delay, 2)
    }
