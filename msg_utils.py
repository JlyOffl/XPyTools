import requests
import json
import uuid

def send_message(msg):
    conversation_id = "1669019186306097152-1770603562751451136"
    message_text = msg
    bearer_token = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    csrf_token = "79e80217d557ef3286fd5024295853d4b45e68423f1b4f84fe701c39ae849ad0634c62c39f2911d03c2e1a4a177196140e00af39e3b5458c07900effb03f25631511697dc197a6c0feb0c06adc63e686"
    transaction_id = "rD9Nvn8ZiZS1qRq9AjlhIvD31CGQemdVHRvLfh8dl2/YjenpjIWmGettiFyn2dsQqLY4ya7w6pytJT9ypXIQVa8CPpAfrw"
    client_uuid = "aa446dd9-c523-4df1-b596-21d2fe7df9e4"

    send_direct_message(conversation_id, message_text, bearer_token, csrf_token, transaction_id, client_uuid)

def send_direct_message(conversation_id, message_text, bearer_token, csrf_token, transaction_id, client_uuid):
    url = "https://x.com/i/api/1.1/dm/new2.json?ext=mediaColor%2CaltText%2CmediaStats%2ChighlightedLabel%2CvoiceInfo%2CbirdwatchPivot%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Carticle&include_ext_alt_text=true&include_ext_limited_action_results=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_groups=true&include_inbox_timelines=true&include_ext_media_color=true&supports_reactions=true"
    
    new_guid = str(uuid.uuid4())

    payload = json.dumps({
        "conversation_id": conversation_id,
        "recipient_ids": False,
        "request_id": new_guid,
        "text": message_text,
        "cards_platform": "Web-12",
        "include_cards": 1,
        "include_quote_count": True,
        "dm_users": False
    })

    headers = {
        'accept': '*/*',
        'accept-language': 'en,en-US;q=0.9',
        'authorization': f'Bearer {bearer_token}',
        'content-type': 'application/json',
        'cookie': '_ga=GA1.2.579883547.1715963901; dnt=1; kdt=inGyOGVqO0eLhYaCiiw9AnQXjvkicrgTykd6MKGM; night_mode=0; lang=en; g_state={"i_l":0}; auth_multi="1669019186306097152:57a1d319bfa07cfa35463bdd94ef29d66503521d|1797340116005920768:c6e3f6751c60aa76d91bd7ded20ec1c9035be42c|1720537712355053568:980622ec79fc8dba97d2d13b790e9c5207d64711|1722724944679694336:67e231f49361246709807405bfff4da242b96827"; auth_token=934c4289886a86c74163f4711ae095036e23d6e4; guest_id_ads=v1%3A172313566157807259; guest_id_marketing=v1%3A172313566157807259; guest_id=v1%3A172313566157807259; twid=u%3D1770603562751451136; ct0=79e80217d557ef3286fd5024295853d4b45e68423f1b4f84fe701c39ae849ad0634c62c39f2911d03c2e1a4a177196140e00af39e3b5458c07900effb03f25631511697dc197a6c0feb0c06adc63e686; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNKB5TKRAToMY3NyZl9p%250AZCIlNjI2YjFhNGNmYzA3NjI3MzhmZDI0MjkxYjQzYjg2M2E6B2lkIiU0NDMw%250AYzE4ZWE2ODk2Y2I1N2I4ZDYxOWY3ZjUxZGE0OA%253D%253D--e8d45fb1d23d2dcc5cae8a9783bdf0219fc7128b; personalization_id="v1_Px0Yl3PyGnd3+jK06Qh/8A=="',
        'origin': 'https://x.com',
        'priority': 'u=1, i',
        'referer': f'https://x.com/messages/{conversation_id}',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-client-transaction-id': transaction_id,
        'x-client-uuid': client_uuid,
        'x-csrf-token': csrf_token,
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'en'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.text

#send_message("This is from my Python")