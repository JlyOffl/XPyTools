import threading
import logging
import random
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks
from rest_utils import *

# === Config ===
DEBUG_MODE = False  # Set to False in production

# === Logging Setup ===
log_level = logging.DEBUG if DEBUG_MODE else logging.ERROR
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# === FastAPI App ===
app = FastAPI()

# ---------------------------
# Helpers
# ---------------------------

def _clean_username(username: str) -> str:
    return (username or "").strip().lstrip("@")

def get_audio_space_link(username: str):
    """
    (Legacy bulk-thread function) Attempts to find and post a space link for the user.
    Guards for missing IDs to avoid /status/None requests.
    """
    try:
        uname = _clean_username(username)
        if not uname:
            return

        if DEBUG_MODE:
            logger.info(f"Started processing for user: {uname}")

        res = get_user_info_by_screen_name(uname)
        if DEBUG_MODE and res:
            logger.info(f"Response for user: {res.text if hasattr(res, 'text') else '<no text>'}")

        if res is None or not getattr(res, "text", ""):
            logger.warning(f"No response received for user: {uname}")
            return

        check = extract_value_from_json_path(res.text, "data")
        if not check:
            logger.warning(f"{uname} - User does not exist")
            DBProxy().DeleteFollower(uname)
            return

        rest_id = extract_value_from_json_path(res.text, "rest_id")
        user_name = extract_value_from_json_path(res.text, "name") or uname
        if not rest_id:
            return

        res = get_space_by_host_id(rest_id)
        DBProxy().UpdateFollowerDisplayName(uname, user_name)

        spacevalue = extract_value_from_json_path(res.text, "users")
        if spacevalue in (None, "{}", "[]"):
            return

        spaceId = extract_value_from_json_path(res.text, "broadcast_id")
        if not spaceId:
            return

        title = extract_value_from_json_path(res.text, "title") or f"{user_name} Space"

        res = get_space_audio_by_id(spaceId)
        if res is None or not getattr(res, "text", ""):
            return

        media_key = extract_value_from_json_path(res.text, "media_key")
        if not media_key:
            return

        res = get_space_audio_link(media_key)
        if res is None or not getattr(res, "text", ""):
            return

        audio_url = extract_value_from_json_path(res.text, "noRedirectPlaybackUrl")
        if not audio_url:
            return

        shortUrl = shorten_url(audio_url)

        tweet = (
            f"Topic: {title}\n"
            f"ID: https://x.com/{uname} ({user_name})\n"
            f"AudioLink: {shortUrl}\n"
            f"Space: https://x.com/i/spaces/{spaceId}"
        )

        try:
            send_telegram_message(tweet)
        except Exception as et:
            logger.warning(f"Telegram send failed for {uname}: {et}")

        # Update display name of host
        try:
            res = get_host_info_by_spaceId(spaceId)
            host_screen_name = extract_value_from_json_path(res.text, "screen_name")
            if host_screen_name:
                res = get_user_info_by_screen_name(host_screen_name)
                host_name = extract_value_from_json_path(res.text, "name")
                if host_name:
                    DBProxy().UpdateFollowerDisplayName(host_screen_name, host_name)
        except Exception as e:
            if DEBUG_MODE:
                logger.info(f"Host display name update failed for {spaceId}: {e}")

    except Exception as e:
        logger.error(f"Error in get_audio_space_link for user {username}: {e}", exc_info=True)

def get_space_info_and_notify(username: str, notify_telegram: bool = True):
    """
    Looks up the user's current Space, builds audio link + short URL,
    optionally sends a Telegram message, and returns a dict with details.
    Returns None if no Space or audio link found.
    """
    try:
        uname = _clean_username(username)
        if not uname:
            return None

        res = get_user_info_by_screen_name(uname)
        if res is None or not getattr(res, "text", ""):
            DBProxy().DeleteFollower(uname)
            return None

        if not extract_value_from_json_path(res.text, "data"):
            DBProxy().DeleteFollower(uname)
            return None

        rest_id  = extract_value_from_json_path(res.text, "rest_id")
        user_name = extract_value_from_json_path(res.text, "name") or uname
        if not rest_id:
            return None

        res = get_space_by_host_id(rest_id)
        DBProxy().UpdateFollowerDisplayName(uname, user_name)

        spacevalue = extract_value_from_json_path(res.text, "users")
        if spacevalue in (None, "{}", "[]"):
            return None

        space_id = extract_value_from_json_path(res.text, "broadcast_id")
        title    = extract_value_from_json_path(res.text, "title") or f"{user_name} Space"
        if not space_id:
            return None

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

        tweet = (
            f"Topic: {title}\n"
            f"ID: https://x.com/{uname} ({user_name})\n"
            f"AudioLink: {short_url}\n"
            f"Space: https://x.com/i/spaces/{space_id}"
        )

        notified = False
        if notify_telegram:
            try:
                send_telegram_message(tweet)
                notified = True
            except Exception as et:
                logger.warning(f"Telegram send failed for {uname}: {et}")

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

def _bulk_spaces_worker(usernames, max_workers: int = 6, delay_range=(1.0, 2.0)):
    """
    Background worker: submits get_audio_space_link for each username,
    with limited concurrency and throttled submission to avoid API floods.
    """
    from concurrent.futures import ThreadPoolExecutor

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for uname in usernames:
                try:
                    executor.submit(get_audio_space_link, uname)
                except Exception as e:
                    logger.warning(f"Failed to submit task for {uname}: {e}")
                # keep the wait to avoid hammering upstream APIs
                time.sleep(random.uniform(*delay_range))
    except Exception as e:
        logger.error(f"Bulk worker failed: {e}", exc_info=True)

# ---------------------------
# HTTP Endpoints
# ---------------------------

@app.get("/spaces/{username}")
def get_space_for_user(username: str):
    """
    GET /spaces/{username}
    Returns short_url (and other details) in JSON AND always sends Telegram.
    """
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
    """
    Bulk trigger over following list.
    - Schedules a background worker that throttles submissions (keeps waits).
    - Returns immediately with the number of users queued.
    """
    try:
        uList = DBProxy().GetFollowingList()
        random.shuffle(uList)
        count = len(uList)

        # Kick off background worker (keeps internal waits and bounded concurrency)
        background_tasks.add_task(_bulk_spaces_worker, uList)

        logger.info(f"XSpacesExplore queued for {count} users")
        return {"status": "X Spaces Explore Triggered", "count": count}

    except Exception as e:
        logger.error(f"Error scheduling /spaces bulk worker: {e}", exc_info=True)
        return {"status": "Failed to start background task", "count": 0}
