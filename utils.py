import json
import os
import threading
import time
import urllib.parse as up
from typing import List

import requests

from db_proxy import DBProxy

SUPPRESS_EMBEDS_FLAG = 4
SEPARATOR = "\n────────────\n"
MAX_DISCORD_CONTENT_LEN = 1900
DISCORD_SENT_IDS_JSON = "discord_sent_ids.json"
DISCORD_IDS_MAX_KEEP = 200
_DISCORD_IDS_LOCK = threading.Lock()


def shorten_url(long_url):
    shorteners = [
        ("https://jly.netlify.app/short", {"url": long_url}),
        ("https://tinyurl.com/api-create.php", {"url": long_url}),
        ("https://clck.ru/--", {"url": long_url}),
    ]
    headers = {"User-Agent": "Mozilla/5.0"}

    for url, params in shorteners:
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            short = response.text.strip()
            if (
                response.status_code == 200
                and short.startswith(("http://", "https://"))
                and "error" not in short.lower()
            ):
                return short
        except requests.RequestException:
            pass

    return None


def send_telegram_message(message):
    token = DBProxy().GetSettingValue("TelegramBotToken")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": DBProxy().GetSettingValue("TelegramChatID"),
        "text": message,
    }
    response = requests.post(url, data=payload, timeout=20)
    return response.json()


def _ensure_wait_true(webhook_url: str) -> str:
    if not webhook_url:
        return webhook_url

    parsed = up.urlparse(webhook_url)
    q = dict(up.parse_qsl(parsed.query, keep_blank_values=True))
    q["wait"] = "true"
    return up.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, up.urlencode(q), parsed.fragment))


def _webhook_delete_url(webhook_url: str, message_id: str) -> str:
    parsed = up.urlparse(webhook_url)
    base = up.urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""))
    return f"{base}/messages/{message_id}"


def _load_discord_sent_ids() -> List[str]:
    try:
        with open(DISCORD_SENT_IDS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return [str(x) for x in data if str(x).strip()]
        return []
    except FileNotFoundError:
        return []
    except Exception:
        return []


def _save_discord_sent_ids(ids: List[str]) -> None:
    try:
        ids = [str(x) for x in ids if str(x).strip()]
        if len(ids) > DISCORD_IDS_MAX_KEEP:
            ids = ids[-DISCORD_IDS_MAX_KEEP:]

        tmp = DISCORD_SENT_IDS_JSON + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(ids, f)
        os.replace(tmp, DISCORD_SENT_IDS_JSON)
    except Exception:
        pass


def _append_sent_id(message_id: str) -> None:
    if not message_id:
        return

    with _DISCORD_IDS_LOCK:
        ids = _load_discord_sent_ids()
        ids.append(str(message_id))
        _save_discord_sent_ids(ids)


def _delete_previous_discord_messages(webhook_url: str) -> None:
    if not webhook_url:
        return

    with _DISCORD_IDS_LOCK:
        ids = _load_discord_sent_ids()

    if not ids:
        return

    remaining: List[str] = []

    for mid in reversed(ids):
        try:
            delete_url = _webhook_delete_url(webhook_url, mid)
            response = requests.delete(delete_url, timeout=10)

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after is None:
                    try:
                        retry_after = response.json().get("retry_after", 1.0)
                    except Exception:
                        retry_after = 1.0

                time.sleep(float(retry_after))
                response = requests.delete(delete_url, timeout=10)

            if response.status_code in (204, 404):
                time.sleep(0.2)
                continue

            remaining.append(mid)
            time.sleep(0.5)

        except Exception:
            remaining.append(mid)
            time.sleep(0.5)

    with _DISCORD_IDS_LOCK:
        _save_discord_sent_ids(remaining)


def _post_webhook_and_store_id(webhook_url: str, payload: dict) -> None:
    webhook_url_wait = _ensure_wait_true(webhook_url)
    response = requests.post(webhook_url_wait, json=payload, timeout=10)

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            try:
                retry_after = response.json().get("retry_after", 1.0)
            except Exception:
                retry_after = 1.0
        time.sleep(float(retry_after))
        response = requests.post(webhook_url_wait, json=payload, timeout=10)

    if response.status_code not in (200, 204):
        raise Exception(f"Discord error {response.status_code}: {response.text}")

    if response.status_code == 200:
        try:
            mid = response.json().get("id")
            if mid:
                _append_sent_id(mid)
        except Exception:
            pass


def send_discord_message(message: str) -> bool:
    message = message.rstrip() + SEPARATOR

    webhook_url = DBProxy().GetSettingValue("DiscordWebhookURL")
    if not webhook_url:
        raise Exception("DiscordWebhookURL setting is missing")

    _delete_previous_discord_messages(webhook_url)

    payload = {
        "content": message,
        "flags": SUPPRESS_EMBEDS_FLAG,
    }

    _post_webhook_and_store_id(webhook_url, payload)
    return True


def _build_one_discord_message(
    blocks: List[str],
    header: str = "",
    separator: str = SEPARATOR,
    max_len: int = MAX_DISCORD_CONTENT_LEN,
) -> str:
    header = (header or "").strip()
    message = (header + "\n") if header else ""

    included = 0
    omitted = 0

    for block in blocks:
        block = (block or "").strip()
        if not block:
            continue

        piece = block + separator

        if len(piece) > max_len:
            room = max_len - len(message) - 60
            if room > 0:
                message += piece[:room].rstrip() + "\n…(truncated)\n"
                included += 1
            else:
                omitted += 1
            omitted += sum(1 for x in blocks[included + omitted :] if (x or "").strip())
            break

        if len(message) + len(piece) > max_len:
            omitted += 1
            continue

        message += piece
        included += 1

    if omitted > 0:
        message = message.rstrip() + f"\n\n⚠️ Omitted {omitted} item(s) due to Discord 2000-char limit."

    return message[:max_len]


def send_discord_message_batch(blocks: List[str], header: str = "", strict_one_message: bool = True) -> bool:
    webhook_url = DBProxy().GetSettingValue("DiscordWebhookURL")
    if not webhook_url:
        raise Exception("DiscordWebhookURL setting is missing")

    _delete_previous_discord_messages(webhook_url)

    def _post(content: str):
        payload = {"content": content, "flags": SUPPRESS_EMBEDS_FLAG}
        _post_webhook_and_store_id(webhook_url, payload)

    if strict_one_message:
        content = _build_one_discord_message(blocks, header=header)
        _post(content)
        return True

    messages: List[str] = []
    current = (header.strip() + "\n") if header else ""

    for block in blocks:
        block = (block or "").strip()
        if not block:
            continue
        piece = block + SEPARATOR

        if len(piece) > MAX_DISCORD_CONTENT_LEN:
            if current.strip():
                messages.append(current.rstrip())
                current = ""
            for i in range(0, len(piece), MAX_DISCORD_CONTENT_LEN):
                messages.append(piece[i : i + MAX_DISCORD_CONTENT_LEN])
            continue

        if len(current) + len(piece) > MAX_DISCORD_CONTENT_LEN:
            messages.append(current.rstrip())
            current = piece
        else:
            current += piece

    if current.strip():
        messages.append(current.rstrip())

    for message in messages:
        _post(message)
        time.sleep(0.35)

    return True


def extract_value_from_json_path(json_data, search_string):
    data = json.loads(json_data)
    matches = []

    def search(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == search_string:
                    matches.append(value)
                search(value)
        elif isinstance(obj, list):
            for item in obj:
                search(item)

    search(data)
    return matches[-1] if matches else None


def extract_value(json_data, path):
    obj = json.loads(json_data)

    for key in path.split("."):
        if not isinstance(obj, dict):
            return None

        obj = obj.get(key)
        if obj is None:
            return None

    return obj
