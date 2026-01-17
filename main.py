import threading
import logging
import random
import time
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

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


def _url_line(url: str, bold: bool = False) -> str:
    """Return URL as-is; bold optional."""
    url = (url or "").strip()
    if not url:
        return ""
    return f"**{url}**" if bold else url


def _user_line(uname: str, display_name: str) -> str:
    """
    iOS-friendly: URL starts the line, display name at end
    Format: https://x.com/user (Display Name)
    """
    u = _clean_username(uname)
    dn = (display_name or "").strip()
    url = f"https://x.com/{u}" if u else ""
    if not url:
        return ""
    return f"{url} ({dn})" if dn else url


def _short_url_block(short_url: str) -> str:
    s = (short_url or "").strip()
    if not s:
        return ""
    return f"**{s}**"

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
# === New: build a single "space record" (for grouping)
# ============================================================
def build_space_record(username: str) -> Optional[Dict[str, Any]]:
    """
    Return a dict record:
      { title, space_id, short_url, uname, display_name }
    Used by bulk to group by space_id.
    """
    try:
        uname = _clean_username(username)
        if not uname:
            return None

        core = _fetch_user_space_core(uname)
        if not core:
            return None
        _, display_name, space_id, title = core

        audio_core = _fetch_audio_core(space_id)
        if not audio_core:
            return None
        _, short_url = audio_core

        return {
            "title": title,
            "space_id": space_id,
            "short_url": short_url,
            "uname": uname,
            "display_name": display_name,
        }

    except Exception as e:
        logger.error(f"build_space_record error for {username}: {e}", exc_info=True)
        return None


def _format_grouped_space_message(title: str, short_url: str, space_id: str, users: List[Tuple[str, str]]) -> str:
    """
    Build ONE message block for a space, with multiple user lines.

    Requirements:
      - No icons
      - short url bold with tiny padding ONLY (thin-space lines)
      - user url + display name in same line
      - URLs remain on their own line for iOS autolinking
    """
    space_link = f"https://x.com/i/spaces/{space_id}"

    lines: List[str] = [f"{title}"]

    # Add tiny spacing only around bold short URL
    lines.append(_short_url_block(short_url).rstrip("\n"))

    # Space URL (on its own line)
    space_line = _url_line(space_link)
    if space_line:
        lines.append(space_line)

    # Users: URL + displayname on one line
    for uname, display_name in users:
        ul = _user_line(uname, display_name)
        if ul:
            lines.append(ul)

    return "\n".join(lines)


# ============================================================
# === Message builder (used by single-user flows)
# ============================================================
def build_space_message(username: str) -> Optional[str]:
    """
    Build the Discord/Telegram message text for a single username.
    Returns message string or None.
    """
    try:
        rec = build_space_record(username)
        if not rec:
            return None

        space_link = f"https://x.com/i/spaces/{rec['space_id']}"

        msg = (
            f"{rec['title']}\n"
            f"{_short_url_block(rec['short_url'])}\n"
            f"{_url_line(space_link)}\n"
            f"{_user_line(rec['uname'], rec['display_name'])}"
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

        space_link = f"https://x.com/i/spaces/{space_id}"

        tweet = (
            f"{title}"
            f"{_short_url_block(short_url)}"
            f"{_url_line(space_link)}\n"
            f"{_user_line(uname, user_name)}"
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
# === Adaptive, overlap-safe bulk worker (GROUPED by space_id)
# ============================================================
def _bulk_spaces_worker(usernames, max_workers: int = 100, delay_range=None):
    """
    Builds space records for each username concurrently, GROUPS by space_id,
    and sends consolidated Discord message(s) with grouped blocks.
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

        records: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=effective_workers) as executor:
            futures = []
            for uname in usernames:
                futures.append(executor.submit(build_space_record, uname))
                time.sleep(random.uniform(*delay_range))

            for f in as_completed(futures):
                try:
                    rec = f.result()
                    if rec:
                        records.append(rec)
                except Exception as e:
                    logger.error(f"Bulk future error: {e}", exc_info=True)

        if not records:
            return

        # Group by space_id
        grouped: Dict[str, Dict[str, Any]] = {}
        for r in records:
            sid = r["space_id"]
            g = grouped.get(sid)
            if not g:
                grouped[sid] = {
                    "title": r["title"],
                    "space_id": sid,
                    "short_url": r["short_url"],
                    "users": [(r["uname"], r["display_name"])],
                }
            else:
                g["users"].append((r["uname"], r["display_name"]))

        blocks: List[str] = []
        for sid in sorted(grouped.keys()):
            g = grouped[sid]

            # dedupe users (keep order)
            seen_u = set()
            uniq_users = []
            for u, dn in g["users"]:
                if u not in seen_u:
                    seen_u.add(u)
                    uniq_users.append((u, dn))
            g["users"] = uniq_users

            blocks.append(
                _format_grouped_space_message(
                    title=g["title"],
                    short_url=g["short_url"],
                    space_id=g["space_id"],
                    users=g["users"],
                )
            )

        ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        header = f"Refresh: {ts}\nSpaces: {len(blocks)} | Users matched: {len(records)}\n"

        send_discord_message_batch(
            blocks,
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
