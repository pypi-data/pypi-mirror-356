import os
import requests
import threading
from . import config
import sys

BASE_URL = os.environ.get("CLDKCTL_BASE_URL", "https://ai.cloudeka.id")

# Thread-safe singleton for session token
class SessionTokenCache:
    _lock = threading.Lock()
    _token = None

    @classmethod
    def get_token(cls, login_token):
        with cls._lock:
            # Try to get from config first
            if cls._token is not None:
                return cls._token
            token_from_config = config.get_config("TOKEN")
            if token_from_config:
                cls._token = token_from_config
                return cls._token
            # If not in config, exchange login token
            session_token = exchange_login_token_for_session_token(login_token)
            if session_token:
                cls._token = session_token
                config.set_config("TOKEN", session_token)
            return cls._token

def exchange_login_token_for_session_token(login_token):
    url = BASE_URL + "/core/cldkctl/auth"
    try:
        resp = requests.post(url, json={"token": login_token})
        resp.raise_for_status()
        data = resp.json()
        # The session token is in data['data']['token']
        session_token = None
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], dict) and "token" in data["data"]:
                session_token = data["data"]["token"]
            elif "token" in data:
                session_token = data["token"]
        if session_token:
            print(f"[INFO] Exchanged login token for session token: {session_token}", file=sys.stderr)  # ← Changed
            return session_token
        else:
            print(f"[ERROR] Could not extract session token from response: {data}", file=sys.stderr)  # ← Changed
            return None
    except Exception as e:
        print(f"[ERROR] Failed to exchange login token for session token: {e}", file=sys.stderr)  # ← Changed
        return None