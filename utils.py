import json
import requests
from db_proxy import *
from datetime import datetime
import subprocess
import random
import string
import time
from typing import List, Optional

def shorten_url(long_url):
    #api_url = f"https://is.gd/create.php?format=simple&url={long_url}"
    #api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
    api_url = f"https://jly.netlify.app/short?url={long_url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def check_process(*strings):
    command = 'ps aux'
    ps_output = subprocess.check_output(command.split()).decode()

    for line in ps_output.splitlines():
        if all(s in line for s in strings):
            #print(f"Process found: {line}")
            return True
    return False

def kill_ffmpeg_processes():
    """
    Kill all running ffmpeg processes.
    """
    try:
        subprocess.run(['pkill', '-f', 'ffmpeg'], check=True)
        print("All ffmpeg processes have been terminated.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while terminating ffmpeg processes: {e}")


def generate_random_string(length=4):
    """
    Generate a random alphanumeric string.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def record_m3u8(url, spaceid, output_pattern="rec-%03d.mp4", segment_time=1800):
    """
    Record an M3U8 URL using ffmpeg.
    Ensures only one recorder per URL.
    """
    if check_process(url, '_Rec_'):
        return

    command = [
        "ffmpeg",
        "-i", url,
        "-c:v", "libx265",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "segment",
        "-segment_time", str(segment_time),
        "-reset_timestamps", "1",
        "-map", "0",
        "-segment_format_options", "movflags=+faststart",
        "-c", "copy",
        f"/home/recordings/{spaceid}_Rec_{output_pattern}"
    ]

    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass


# ============================================================
# === Telegram Messaging (unchanged)
# ============================================================

def send_telegram_message(message):
    """
    Send a Telegram message using stored bot token & chat ID.
    """
    message = message.replace("https://tinyurl.com/", " @")
    token = DBProxy().GetSettingValue('TelegramBotToken')
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': DBProxy().GetSettingValue('TelegramChatID'),
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


# ============================================================
# === Discord Webhook Messaging (WITH DELETE + JSON STORAGE)
# ============================================================

SUPPRESS_EMBEDS_FLAG = 4
SEPARATOR = "\n────────────\n"
MAX_DISCORD_CONTENT_LEN = 1900

# Store sent webhook message IDs in CURRENT folder
DISCORD_SENT_IDS_JSON = "discord_sent_ids.json"

# Safety limit for stored IDs
DISCORD_IDS_MAX_KEEP = 50


def _ensure_wait_true(webhook_url: str) -> str:
    """
    Ensure ?wait=true is present so Discord returns message JSON (id).
    """
    parsed = urlparse(webhook_url)
    q = dict(parse_qsl(parsed.query))
    q["wait"] = "true"
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(q), parsed.fragment))


def _webhook_delete_url(webhook_url: str, message_id: str) -> str:
    """
    Build webhook delete URL:
    {webhook_url}/messages/{message_id}
    """
    parsed = urlparse(webhook_url)
    base = urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""))
    return f"{base}/messages/{message_id}"


def _load_discord_sent_ids() -> List[str]:
    """
    Load stored webhook message IDs from JSON file.
    """
    try:
        with open(DISCORD_SENT_IDS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [str(x) for x in data if str(x).strip()]
    except Exception:
        return []


def _save_discord_sent_ids(ids: List[str]) -> None:
    """
    Save webhook message IDs to JSON file.
    """
    try:
        ids = ids[-DISCORD_IDS_MAX_KEEP:]
        with open(DISCORD_SENT_IDS_JSON, "w", encoding="utf-8") as f:
            json.dump(ids, f)
    except Exception:
        pass


def _append_sent_id(message_id: str) -> None:
    """
    Append a newly sent webhook message ID.
    """
    ids = _load_discord_sent_ids()
    ids.append(message_id)
    _save_discord_sent_ids(ids)


def _delete_previous_discord_messages(webhook_url: str) -> None:
    """
    Delete all previously sent webhook messages
    using stored message IDs.
    """
    ids = _load_discord_sent_ids()
    if not ids:
        return

    remaining = []
    for mid in ids:
        try:
            r = requests.delete(_webhook_delete_url(webhook_url, mid), timeout=10)

            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After", 1)
                time.sleep(float(retry_after))
                r = requests.delete(_webhook_delete_url(webhook_url, mid), timeout=10)

            if r.status_code not in (204, 404):
                remaining.append(mid)

            time.sleep(0.2)

        except Exception:
            remaining.append(mid)

    _save_discord_sent_ids(remaining)


def send_discord_message(message: str) -> bool:
    """
    Send ONE Discord webhook message.
    Deletes old webhook messages first.
    """
    webhook_url = DBProxy().GetSettingValue('DiscordWebhookURL')
    webhook_url_wait = _ensure_wait_true(webhook_url)

    _delete_previous_discord_messages(webhook_url)

    payload = {
        "content": message.rstrip() + SEPARATOR,
        "flags": SUPPRESS_EMBEDS_FLAG
    }

    r = requests.post(webhook_url_wait, json=payload, timeout=10)

    if r.status_code == 200:
        mid = r.json().get("id")
        if mid:
            _append_sent_id(mid)

    return True


def _build_one_discord_message(blocks: List[str], header: str = "") -> str:
    """
    Build exactly ONE Discord message (<= 2000 chars).
    """
    msg = (header + "\n") if header else ""

    for b in blocks:
        piece = b.strip() + SEPARATOR
        if len(msg) + len(piece) > MAX_DISCORD_CONTENT_LEN:
            break
        msg += piece

    return msg[:MAX_DISCORD_CONTENT_LEN]


def send_discord_message_batch(
    blocks: List[str],
    header: str = "",
    strict_one_message: bool = True
) -> bool:
    """
    Send batched Discord webhook messages.
    Deletes previous messages before sending new ones.
    """
    webhook_url = DBProxy().GetSettingValue('DiscordWebhookURL')
    webhook_url_wait = _ensure_wait_true(webhook_url)

    _delete_previous_discord_messages(webhook_url)

    def _post(content):
        r = requests.post(
            webhook_url_wait,
            json={"content": content, "flags": SUPPRESS_EMBEDS_FLAG},
            timeout=10
        )
        if r.status_code == 200:
            mid = r.json().get("id")
            if mid:
                _append_sent_id(mid)

    if strict_one_message:
        _post(_build_one_discord_message(blocks, header))
        return True

    current = header + "\n" if header else ""
    for b in blocks:
        piece = b.strip() + SEPARATOR
        if len(current) + len(piece) > MAX_DISCORD_CONTENT_LEN:
            _post(current)
            current = piece
        else:
            current += piece

    if current.strip():
        _post(current)

    return True


# ============================================================
# === Telegram Cleanup Utilities (unchanged)
# ============================================================

def get_chat_history(bot_token, chat_id, limit=100):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url, params={"limit": limit})
    return response.json().get("result", [])


def delete_message(bot_token, chat_id, message_id):
    url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    return requests.post(url, params={"chat_id": chat_id, "message_id": message_id})


def clear_messages():
    bot_token = DBProxy().GetSettingValue('TelegramBotToken')
    chat_id = DBProxy().GetSettingValue('TelegramChatID')

    for msg in get_chat_history(bot_token, chat_id):
        if 'message' in msg:
            delete_message(bot_token, chat_id, msg['message']['message_id'])


# ============================================================
# === Misc Helpers (unchanged)
# ============================================================

def get_timestamp(format_type='standard'):
    now = datetime.now()
    if format_type == 'standard':
        return now.strftime("%Y-%m-%d %H:%M:%S")
    if format_type == 'iso':
        return now.isoformat()
    if format_type == 'custom':
        return now.strftime("%Y%m%d_%H%M%S")
    raise ValueError("Invalid format type.")


def extract_value_from_json_path(json_data, search_string):
    data = json.loads(json_data)

    def search(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == search_string:
                    return v
                r = search(v)
                if r is not None:
                    return r
        elif isinstance(obj, list):
            for i in obj:
                r = search(i)
                if r is not None:
                    return r
        return None

    return search(data)


def get_header_value(file_path, key):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith(f"-H '{key}:"):
                return line.split(": ", 1)[1].strip(" '\\")
