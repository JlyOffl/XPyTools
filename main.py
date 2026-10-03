import json
import logging
import random
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from fastapi import BackgroundTasks, FastAPI, HTTPException

from rest_utils import (
    DBProxy,
    extract_value,
    extract_value_from_json_path,
    get_host_info_by_spaceId,
    get_space_audio_by_id,
    get_space_audio_link,
    get_space_by_host_id,
    get_user_info_by_screen_name,
    send_discord_message_batch,
    send_telegram_message,
    shorten_url,
)

DEBUG_MODE = False

log_level = logging.DEBUG if DEBUG_MODE else logging.ERROR
logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

_RUNNING_BULK = threading.Event()


def _clean_username(username: str) -> str:
    return (username or "").strip().lstrip("@")


def _url_line(url: str, bold: bool = False) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    return f"**{url}**" if bold else url


def _user_line(uname: str, display_name: str) -> str:
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


def _fetch_user_space_core(uname: str):
    res = get_user_info_by_screen_name(uname)
    if res is None or not getattr(res, "text", ""):
        DBProxy().DeleteFollower(uname)
        return None

    try:
        user_data = json.loads(res.text)
    except json.JSONDecodeError:
        DBProxy().DeleteFollower(uname)
        return None

    if not user_data or user_data.get("data") in (None, {}) or user_data.get("errors"):
        DBProxy().DeleteFollower(uname)
        return None

    rest_id = extract_value_from_json_path(res.text, "rest_id")
    display_name = extract_value(res.text, "data.user.result.legacy.name") or extract_value(
        res.text, "data.user.result.core.name"
    ) or uname
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


def _upsert_host_for_space(space_id: str) -> None:
    try:
        res = get_host_info_by_spaceId(space_id)
        screen_name = extract_value_from_json_path(res.text, "screen_name")
        if screen_name:
            DBProxy().UpsertFollower(screen_name)
    except Exception:
        pass


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

    _upsert_host_for_space(space_id)

    short_url = shorten_url(audio_url)
    return audio_url, short_url


def build_space_record(username: str) -> Optional[Dict[str, Any]]:
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


def _format_grouped_space_message(
    title: str, short_url: str, space_id: str, users: List[Tuple[str, str]]
) -> str:
    space_link = f"https://x.com/i/spaces/{space_id}"

    lines: List[str] = [f"{title}"]

    su = _short_url_block(short_url)
    if su:
        lines.append(su)

    space_line = _url_line(space_link)
    if space_line:
        lines.append(space_line)

    # for uname, display_name in users:
    #     ul = _user_line(uname, display_name)
    #     if ul:
    #         lines.append(ul)

    return "\n".join(lines)


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

        space_link = f"https://x.com/i/spaces/{space_id}"

        tweet = (
            f"{title}\n"
            f"{_short_url_block(short_url)}\n"
            f"{_url_line(space_link)}\n"
            f"{_user_line(uname, user_name)}"
        )

        notified = False
        if notify_telegram:
            threading.Thread(target=lambda: send_telegram_message(tweet), daemon=True).start()
            notified = True

        return {
            "username": uname,
            "display_name": user_name,
            "space_id": space_id,
            "title": title,
            "audio_url": audio_url,
            "short_url": short_url,
            "tweet": tweet,
            "notified": notified,
        }

    except Exception as e:
        logger.error(f"get_space_info_and_notify error for {username}: {e}", exc_info=True)
        return None


def _bulk_spaces_worker(usernames, max_workers: int = 100, delay_range=None):
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

        logger.info(f"Number of blocks: {len(blocks)}")
        ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        header = f"Refresh: {ts}\nSpaces: {len(blocks)} | Users matched: {len(records)}\n"

        send_discord_message_batch(blocks, header=header, strict_one_message=False)

    finally:
        _RUNNING_BULK.clear()


@app.get("/spaces/{username}")
def get_space_for_user(username: str):
    if not username or not username.strip():
        raise HTTPException(status_code=400, detail="Username is required.")

    info = get_space_info_and_notify(username, notify_telegram=True)
    if not info:
        return {"status": "No space/audio found", "username": _clean_username(username)}

    return {
        "status": "Success",
        **{
            k: info[k]
            for k in (
                "username",
                "display_name",
                "space_id",
                "title",
                "short_url",
                "notified",
            )
        },
    }


@app.get("/spaces")
def fetch_space(background_tasks: BackgroundTasks):
    if _RUNNING_BULK.is_set():
        return {"status": "Already running", "in_progress": True}

    ulist = DBProxy().GetFollowingList()
    random.shuffle(ulist)

    delay = random.uniform(0, 5)

    background_tasks.add_task(lambda: (time.sleep(delay), _bulk_spaces_worker(ulist)))

    return {"status": "Triggered", "count": len(ulist), "jitter_seconds": round(delay, 2)}

@app.get("/is")
def is():
    return "Y"