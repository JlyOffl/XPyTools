import json
import requests
from db_proxy import *
from datetime import datetime
import subprocess
import random
import string

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
