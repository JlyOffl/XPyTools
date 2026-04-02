import requests
import random
import os
import json
import datetime
from utils import *
from rest_core import *

def execute_api(url, method, payload):
    import os, re, random, requests

    # --- resolve Settings folder relative to this file ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    settings_dir = os.path.join(base_dir, "Settings")

    # gather all regular files in Settings
    inf_files = [
        os.path.join(settings_dir, f)
        for f in os.listdir(settings_dir)
        if os.path.isfile(os.path.join(settings_dir, f))
    ]
    random.shuffle(inf_files)

    # --- tiny helpers (scoped) ---
    def _parse_curl_inf(path: str):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        # -H 'Header: value'
        headers = {}
        for m in re.finditer(r"-H\s+'([^']+)'", text):
            raw = m.group(1)
            if ":" in raw:
                k, v = raw.split(":", 1)
                headers[k.strip()] = v.strip()

        # prefer -b '...'; else fall back to cookie header
        m_cookie = re.search(r"-b\s+'([^']+)'", text)
        if m_cookie:
            cookie_str = m_cookie.group(1).strip()
        else:
            cookie_str = headers.get("cookie") or headers.get("Cookie") or ""

        # dequote
        def dequote(v: str) -> str:
            return v[1:-1] if isinstance(v, str) and len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"') else v

        for k in list(headers.keys()):
            headers[k] = dequote(headers[k])
        cookie_str = dequote(cookie_str)

        # if cookie came from header, remove it from headers (we'll use session cookies)
        headers.pop("cookie", None)
        headers.pop("Cookie", None)

        return headers, cookie_str

    def _cookie_str_to_dict(cookie_str: str) -> dict:
        parts = [p.strip() for p in (cookie_str or "").split(";") if "=" in p]
        cookies = {}
        for p in parts:
            k, v = p.split("=", 1)
            cookies[k.strip()] = v
        return cookies

    def _clean_headers(h: dict) -> dict:
        return {k: str(v) for k, v in h.items() if v not in (None, "", [])}

    res = None

    for inf_path in inf_files:
        try:
            hdrs_from_inf, cookie_str = _parse_curl_inf(inf_path)
            cookies = _cookie_str_to_dict(cookie_str)
            ct0 = cookies.get("ct0")
            if not ct0:
                # malformed cookie blob; try next file
                continue

            # force x-csrf-token == ct0
            x_csrf = hdrs_from_inf.get("x-csrf-token") or ct0

            headers = _clean_headers({
                "authority": "x.com",
                "accept": hdrs_from_inf.get("accept", "*/*"),
                "accept-language": hdrs_from_inf.get("accept-language", "en,en-US;q=0.9"),
                "content-type": "application/json",
                "referer": hdrs_from_inf.get("referer", "https://x.com/"),
                "if-none-match": hdrs_from_inf.get("if-none-match", "d3a398f9ab5332ecf1d7312dba0465c3"),
                "priority": hdrs_from_inf.get("priority", "u=1, i"),
                "sec-ch-ua": hdrs_from_inf.get("sec-ch-ua", "\"Google Chrome\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\""),
                "sec-ch-ua-mobile": hdrs_from_inf.get("sec-ch-ua-mobile", "?0"),
                "sec-ch-ua-platform": hdrs_from_inf.get("sec-ch-ua-platform", "\"Windows\""),
                "sec-fetch-dest": hdrs_from_inf.get("sec-fetch-dest", "empty"),
                "sec-fetch-mode": hdrs_from_inf.get("sec-fetch-mode", "cors"),
                "sec-fetch-site": hdrs_from_inf.get("sec-fetch-site", "same-origin"),
                "user-agent": hdrs_from_inf.get("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"),
                "x-client-transaction-id": hdrs_from_inf.get("x-client-transaction-id"),
                "x-client-uuid": hdrs_from_inf.get("x-client-uuid"),
                "x-csrf-token": x_csrf,
                "x-twitter-active-user": hdrs_from_inf.get("x-twitter-active-user", "yes"),
                "x-twitter-auth-type": hdrs_from_inf.get("x-twitter-auth-type", "OAuth2Session"),
                "x-twitter-client-language": hdrs_from_inf.get("x-twitter-client-language", "en"),
                "authorization": hdrs_from_inf.get("authorization") or hdrs_from_inf.get("Authorization"),
                "x-xp-forwarded-for": hdrs_from_inf.get("x-xp-forwarded-for"),
            })

            # FIXED LINE: removed extra ')'
            session = requests.Session()
            session.cookies.update(cookies)

            m = (method or "GET").upper()
            if m == "GET":
                res = session.get(url, headers=headers, timeout=60)
            elif m == "POST":
                if isinstance(payload, (dict, list)):
                    res = session.post(url, headers=headers, json=payload, timeout=60)
                else:
                    res = session.post(url, headers=headers, data=payload, timeout=60)
            else:
                res = session.request(m, url, headers=headers, data=payload, timeout=60)

            # Acceptable success: 200 and not rate-limited text
            if res is not None and res.status_code == 200 and res.text.strip() != "Rate limit exceeded":
                # print(f"Successful API call with {inf_path}")
                break

            # If it's a hard failure that's not worth rotating further, break; else try next file
            if res is not None and res.status_code not in (401, 403, 429, 500, 502, 503, 504):
                break

        except Exception:
            # skip bad/malformed file and continue
            continue

    return res
    
def get_space_audio_link(mediaKey):

    return execute_api(f"https://x.com/i/api/1.1/live_video_stream/status/{mediaKey}?client=web&use_syndication_guest_id=false&cookie_set_host=twitter.com", "GET", {})
    
def get_space_audio_by_id(spaceId):

    return execute_api(f"https://x.com/i/api/graphql/BejkHZ2sEvzRn2IWE0Et8Q/AudioSpaceById?variables=%7B%22id%22%3A%22{spaceId}%22%2C%22isMetatagsQuery%22%3Atrue%2C%22withReplays%22%3Atrue%2C%22withListeners%22%3Atrue%7D&features=%7B%22spaces_2022_h2_spaces_communities%22%3Atrue%2C%22spaces_2022_h2_clipping%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22responsive_web_profile_redirect_enabled%22%3Afalse%2C%22rweb_tipjar_consumption_enabled%22%3Afalse%2C%22verified_phone_label_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22responsive_web_grok_analyze_post_followups_enabled%22%3Atrue%2C%22responsive_web_jetfuel_frame%22%3Atrue%2C%22responsive_web_grok_share_attachment_enabled%22%3Atrue%2C%22responsive_web_grok_annotations_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22content_disclosure_indicator_enabled%22%3Atrue%2C%22content_disclosure_ai_generated_indicator_enabled%22%3Atrue%2C%22responsive_web_grok_show_grok_translated_post%22%3Atrue%2C%22responsive_web_grok_analysis_button_from_backend%22%3Atrue%2C%22post_ctas_fetch_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Afalse%2C%22responsive_web_grok_image_annotation_enabled%22%3Atrue%2C%22responsive_web_grok_imagine_annotation_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_grok_community_note_auto_translation_is_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D", "GET", {})
    
def get_space_by_host_id(UserId):

    return execute_api(f"https://x.com/i/api/fleets/v1/avatar_content?user_ids={UserId}&only_spaces=true", "GET", {})
    
def get_user_info_by_screen_name(screen_name):

    return execute_api(f"https://x.com/i/api/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName?variables=%7B%22screen_name%22%3A%22{screen_name}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D", "GET", {})
    
def get_host_info_by_spaceId(spaceId):

    return execute_api(f"https://x.com/i/api/graphql/d03OdorPdZ_sH9V3D1_yWQ/AudioSpaceById?variables=%7B%22id%22%3A%22{spaceId}%22%2C%22isMetatagsQuery%22%3Afalse%2C%22withReplays%22%3Atrue%2C%22withListeners%22%3Atrue%7D&features=%7B%22spaces_2022_h2_spaces_communities%22%3Atrue%2C%22spaces_2022_h2_clipping%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D", "GET", {})
    
def get_space_info(spaceId):
    
    return execute_api(f"https://x.com/i/api/graphql/_Gr0XVkpTrRyGrf5P4cktA/AudioSpaceById?variables=%7B%22id%22%3A%22{spaceId}%22%2C%22isMetatagsQuery%22%3Atrue%2C%22withReplays%22%3Atrue%2C%22withListeners%22%3Atrue%7D&features=%7B%22spaces_2022_h2_spaces_communities%22%3Atrue%2C%22spaces_2022_h2_clipping%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D", "GET", {})