import requests
import time

_config = {
    "token": None,
    "wait": 0
}

_last_response = None

def config(token: str, wait: float = 0):
    _config["token"] = token
    _config["wait"] = wait

def search(username: str):
    global _last_response
    if not _config["token"]:
        raise ValueError("Token is not configured. Use config(token=...) first.")
    
    username = username.lstrip('@')

    url = f"https://sqx.pythonanywhere.com/api/v0/@user/{username}"
    headers = {
        "Authorization": f"Token {_config['token']}"
    }

    if _config["wait"]:
        time.sleep(_config["wait"])

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        _last_response = response.json()
    except requests.exceptions.RequestException as e:
        _last_response = {"error": str(e)}

    return _last_response

class TikTokUserInfo:
    pass 
