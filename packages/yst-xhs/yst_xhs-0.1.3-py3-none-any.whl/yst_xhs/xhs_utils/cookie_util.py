import json

def trans_cookies(cookies_str):
    if cookies_str.startswith("{") and cookies_str.endswith("}"):
        return json.loads(cookies_str)
    
    cookies = {}
    for cookie in cookies_str.split("; "):
        cookies[cookie.split("=")[0]] = cookie.split("=")[1]
    return cookies
