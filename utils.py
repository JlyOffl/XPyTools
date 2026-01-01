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
    # Define the characters to choose from: digits and letters (both lowercase and uppercase)
    characters = string.ascii_letters + string.digits
    # Use random.choices to pick random characters from the set
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def record_m3u8(url, spaceid, output_pattern="rec-%03d.mp4", segment_time=1800):
    """
    Record an M3U8 URL using ffmpeg.

    Args:
        url (str): The M3U8 URL to record.
        output_pattern (str): The output filename pattern.
        segment_time (int): The length of each segment in seconds.

    Returns:
        None
    """
    if check_process(url, '_Rec_'):
        #print(f"Recording is already running for URL {url}")
        return

    #print("check")
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m")

    # Define the ffmpeg command
    command = [
        "ffmpeg",
        "-i", url,
        "-c:v", "libx265",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "segment",
        "-segment_time", "1800",
        "-reset_timestamps", "1",
        "-map", "0",
        "-segment_format_options", "movflags=+faststart",
        "-c", "copy",
        "/home/recordings/" + spaceid + "_Rec_" + output_pattern
    ]

    try:
        # Run the command in a separate process without waiting for it to finish
        # and without printing the console output of ffmpeg
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        #print(f"Recording started for {url}")
    except subprocess.CalledProcessError as e:
        pass
        #print(f"An error occurred: {e}")

def send_telegram_message(message):
    message = message.replace("https://tinyurl.com/", " @")
    token = DBProxy().GetSettingValue('TelegramBotToken')
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': DBProxy().GetSettingValue('TelegramChatID'),
        'text': message
    }
    response = requests.post(url, data=payload)
    #print (response.text)
    return response.json()

# ============================================================
# === Discord Webhook Messaging
# ============================================================
SUPPRESS_EMBEDS_FLAG = 4
SEPARATOR = "\n────────────\n"
MAX_DISCORD_CONTENT_LEN = 1900  # Discord message content limit

def send_discord_message(message: str) -> bool:
    """
    Send a single Discord webhook message (with separator appended).
    Suppresses link previews (embeds).
    """
    message = (message or "").replace("https://tinyurl.com/", " @")
    message = message.rstrip() + SEPARATOR

    webhook_url = DBProxy().GetSettingValue('DiscordWebhookURL')

    payload = {
        "content": message,
        "flags": SUPPRESS_EMBEDS_FLAG  # no link previews
    }

    response = requests.post(webhook_url, json=payload, timeout=10)

    if response.status_code not in (200, 204):
        raise Exception(f"Discord error {response.status_code}: {response.text}")

    return True


def _build_one_discord_message(
    blocks: List[str],
    header: str = "",
    separator: str = SEPARATOR,
    max_len: int = MAX_DISCORD_CONTENT_LEN
) -> str:
    """
    Build exactly ONE Discord message (<= 2000 chars).
    If content would exceed limit, it truncates and appends an 'omitted' line.
    """
    header = (header or "").strip()
    msg = (header + "\n") if header else ""

    included = 0
    omitted = 0

    for b in blocks:
        b = (b or "").replace("https://tinyurl.com/", " @").strip()
        if not b:
            continue

        piece = b + separator

        # If a single block is too big, truncate that block.
        if len(piece) > max_len:
            # Leave room for note
            room = max_len - len(msg) - 60
            if room > 0:
                msg += piece[:room].rstrip() + "\n…(truncated)\n"
                included += 1
            else:
                omitted += 1
            # everything after is omitted
            omitted += sum(1 for x in blocks[included+omitted:] if (x or "").strip())
            break

        if len(msg) + len(piece) > max_len:
            omitted += 1
            continue

        msg += piece
        included += 1

    if omitted > 0:
        msg = msg.rstrip() + f"\n\n⚠️ Omitted {omitted} item(s) due to Discord 2000-char limit."
    return msg[:max_len]


def send_discord_message_batch(
    blocks: List[str],
    header: str = "",
    strict_one_message: bool = True
) -> bool:
    """
    Send a consolidated Discord message for a batch.

    If strict_one_message=True (default):
      - Sends exactly ONE message, truncating/omitting overflow with a note.

    If strict_one_message=False:
      - Sends as many messages as needed (chunked to 2000 chars each).
    """
    webhook_url = DBProxy().GetSettingValue('DiscordWebhookURL')

    def _post(content: str):
        payload = {"content": content, "flags": SUPPRESS_EMBEDS_FLAG}
        r = requests.post(webhook_url, json=payload, timeout=10)
        if r.status_code == 429:
            # respect retry_after
            retry_after = r.headers.get("Retry-After")
            if retry_after is None:
                try:
                    retry_after = r.json().get("retry_after", 1.0)
                except Exception:
                    retry_after = 1.0
            time.sleep(float(retry_after))
            r = requests.post(webhook_url, json=payload, timeout=10)

        if r.status_code not in (200, 204):
            raise Exception(f"Discord error {r.status_code}: {r.text}")

    if strict_one_message:
        content = _build_one_discord_message(blocks, header=header)
        _post(content)
        return True

    # Chunked mode (multiple messages if needed)
    messages = []
    current = (header.strip() + "\n") if header else ""
    for b in blocks:
        b = (b or "").replace("https://tinyurl.com/", " @").strip()
        if not b:
            continue
        piece = b + SEPARATOR

        if len(piece) > MAX_DISCORD_CONTENT_LEN:
            # flush current, then hard-split the big piece
            if current.strip():
                messages.append(current.rstrip())
                current = ""
            for i in range(0, len(piece), MAX_DISCORD_CONTENT_LEN):
                messages.append(piece[i:i + MAX_DISCORD_CONTENT_LEN])
            continue

        if len(current) + len(piece) > MAX_DISCORD_CONTENT_LEN:
            messages.append(current.rstrip())
            current = piece
        else:
            current += piece

    if current.strip():
        messages.append(current.rstrip())

    for m in messages:
        _post(m)
        time.sleep(0.35)

    return True


def get_chat_history(bot_token, chat_id, limit=100):
    """Retrieve chat history using getUpdates."""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {
        "limit": limit,
        "allowed_updates": ["message"]
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['ok']:
        return data['result']
    else:
        print("Error retrieving messages:", data)
        return []

def delete_message(bot_token, chat_id, message_id):
    """Delete a specific message."""
    url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    params = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(url, params=params)
    data = response.json()

    if data['ok']:
        print(f"Deleted message {message_id}")
    else:
        print(f"Failed to delete message {message_id}: {data}")

def clear_messages():

    bot_token = DBProxy().GetSettingValue('TelegramBotToken')
    chat_id = DBProxy().GetSettingValue('TelegramChatID')

    """Clear all messages in a chat."""
    messages = get_chat_history(bot_token, chat_id)

    for update in messages:
        if 'message' in update and update['message']['chat']['id'] == chat_id:
            message_id = update['message']['message_id']
            delete_message(bot_token, chat_id, message_id)

def get_timestamp(format_type='standard'):
        """
        Generates a timestamp string.

        :param format_type: str, type of format for the timestamp. Options: 'standard', 'iso', 'custom'
        :return: str, formatted timestamp string
        """
        now = datetime.now()

        if format_type == 'standard':
            return now.strftime("%Y-%m-%d %H:%M:%S")
        elif format_type == 'iso':
            return now.isoformat()
        elif format_type == 'custom':
            return now.strftime("%Y%m%d_%H%M%S")
        else:
            raise ValueError("Invalid format type. Choose from 'standard', 'iso', 'custom'.")


def extract_value_from_json_path(json_data, search_string):

    # Parse JSON
    data = json.loads(json_data)

    # Initialize result variable
    result = None

    # Function to recursively search for the string in the JSON keys
    def search(obj, search_string):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == search_string:
                    return value
                else:
                    result = search(value, search_string)
                    if result is not None:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = search(item, search_string)
                if result is not None:
                    return result
        return None

    # Call the search function with the JSON data
    result = search(data, search_string)

    return result

# Define the function to extract header value by key
def get_header_value(file_path, key):
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith(f'-H \'{key}:'):
                return line.strip().split(": ")[1].strip().rstrip('\' \\').lstrip('\' \\').strip()  # Remove leading and trailing ' characters and spaces
