import requests

# Replace with your actual bot token and channel username
TOKEN = "8064082806:AAFZKJFYusz0htNo5JeLQAlNQA8WWLbulVc"
CHANNEL_ID = "-1002479785946"  # Channel username or ID (e.g., @MyChannel)
VIDEO_PATH = "C:\\BK-USLP211\\Src\\test\\3MG.mp4"

def upload_video(token, channel_id, video_path, caption="Check out this video!"):
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    try:
        # Open the video file in binary mode
        with open(video_path, "rb") as video_file:
            # Prepare the payload
            payload = {
                "chat_id": channel_id,
                "caption": caption,
                "supports_streaming": True  # Allows streaming directly in Telegram
            }
            # Prepare the files
            files = {
                "video": video_file
            }
            # Make the POST request
            response = requests.post(url, data=payload, files=files)
            
            # Check the response
            if response.status_code == 200:
                print("Video uploaded successfully!")
                print(response.json())
            else:
                print(f"Failed to upload video: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
upload_video(TOKEN, CHANNEL_ID, VIDEO_PATH)
