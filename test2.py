# pip install httpx==0.27.2
# For HTTP/2 support: pip install "httpx[http2]"
import re
import json
import httpx

FLEETLINE_URL = "https://x.com/i/api/fleets/v1/fleetline"
FLEETLINE_QS  = {"only_spaces": "true"}

# ----------------- curl .inf parsing -----------------

def load_auth_from_curl_inf(path: str) -> dict:
    """
    Parse a saved curl command file that contains lines like:
      -H 'Header-Name: value'
      -b 'cookie1=a; ct0=...; auth_token=...'
    Returns a dict of interesting auth values.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Grab all -H '...'
    header_pairs = {}
    for m in re.finditer(r"-H\s+'([^']+)'", text):
        raw = m.group(1)
        if ":" in raw:
            k, v = raw.split(":", 1)
            header_pairs[k.strip()] = v.strip()

    # Grab -b '...'
    m_cookie = re.search(r"-b\s+'([^']+)'", text)
    cookie_str = m_cookie.group(1).strip() if m_cookie else ""

    # Map to the keys our caller expects
    out = {
        "authorization":           header_pairs.get("authorization") or header_pairs.get("Authorization"),
        "cookie":                  cookie_str,
        "x-client-transaction-id": header_pairs.get("x-client-transaction-id"),
        "x-client-uuid":           header_pairs.get("x-client-uuid"),
        "x-csrf-token":            header_pairs.get("x-csrf-token") or header_pairs.get("ct0"),
        "x-xp-forwarded-for":      header_pairs.get("x-xp-forwarded-for"),
        "if-none-match":           header_pairs.get("if-none-match"),
        # handy to carry through (used to set referer below)
        "_referer":                header_pairs.get("referer"),
    }
    # Strip any surrounding quotes the curl exporter might have left
    for k, v in list(out.items()):
        if isinstance(v, str) and len(v) >= 2 and ((v[0] == v[-1] == "'") or (v[0] == v[-1] == '"')):
            out[k] = v[1:-1]
    return out

# ----------------- helpers -----------------

def cookie_str_to_dict(cookie_str: str) -> dict:
    if not cookie_str or not isinstance(cookie_str, str):
        raise ValueError("Missing cookie string (from -b '...') in the .inf file.")
    parts = [p.strip() for p in cookie_str.split(";") if "=" in p]
    cookies = {}
    for p in parts:
        k, v = p.split("=", 1)
        cookies[k.strip()] = v
    return cookies

def _clean_headers(h: dict) -> dict:
    return {k: str(v) for k, v in h.items() if v not in (None, "", [])}

def _clean_handle(handle: str) -> str:
    handle = (handle or "").strip()
    return handle[1:] if handle.startswith("@") else handle

def build_headers(auth_values: dict, referer_handle: str) -> tuple[dict, dict]:
    authorization = auth_values.get("authorization")
    cookie_str    = auth_values.get("cookie")
    if not authorization:
        raise ValueError("Missing authorization header in .inf (-H 'authorization: Bearer ...').")
    cookies = cookie_str_to_dict(cookie_str)
    ct0 = cookies.get("ct0")
    if not ct0:
        raise ValueError("Cookie string missing 'ct0'. Ensure your -b '...' includes ct0=...")

    # x-csrf-token MUST equal ct0
    x_csrf = auth_values.get("x-csrf-token") or ct0

    # prefer the referer from the .inf if present, else build from handle
    referer = auth_values.get("_referer") or f"https://x.com/{_clean_handle(referer_handle)}"

    raw_headers = {
        "authority": "x.com",
        "accept": "*/*",
        "accept-language": "en,en-US;q=0.9",
        "content-type": "application/json",
        "referer": referer,
        "if-none-match": auth_values.get("if-none-match", "d3a398f9ab5332ecf1d7312dba0465c3"),
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "x-client-transaction-id": auth_values.get("x-client-transaction-id"),
        "x-client-uuid": auth_values.get("x-client-uuid"),
        "x-csrf-token": x_csrf,
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "authorization": authorization,  # keep exactly as captured (do not (de)encode)
        "x-xp-forwarded-for": auth_values.get("x-xp-forwarded-for"),
    }
    return _clean_headers(raw_headers), cookies

def request_fleetline(auth_values: dict, referer_handle: str = "mathu2l"):
    headers, cookies = build_headers(auth_values, referer_handle)
    try:
        with httpx.Client(http2=True, timeout=20.0, follow_redirects=True) as client:
            client.cookies.update(cookies)
            r = client.get(FLEETLINE_URL, params=FLEETLINE_QS, headers=headers)
    except ImportError:
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            client.cookies.update(cookies)
            r = client.get(FLEETLINE_URL, params=FLEETLINE_QS, headers=headers)

    if r.status_code == 403:
        print("403 response headers:", dict(r.headers))
        try:
            print("403 body:", r.json())
        except Exception:
            print("403 body (text):", r.text[:1000])
    r.raise_for_status()
    return r.json()

# ----------------- run -----------------

if __name__ == "__main__":
    inf_path = r"C:\Projects\Git\XPyTools\Settings\MKS1.inf"
    auth_values = load_auth_from_curl_inf(inf_path)
    data = request_fleetline(auth_values, "mathu2l")
    print(json.dumps(data, indent=2))
