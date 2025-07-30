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
    def get_token(cls, login_token=None):
        with cls._lock:
            # Try to get from config first
            if cls._token is not None:
                return cls._token
            token_from_config = config.get_config("TOKEN")
            if token_from_config:
                cls._token = token_from_config
                return cls._token
            # If not in config, exchange login token
            if not login_token:
                login_token = config.get_config("AUTH")
            session_token = exchange_login_token_for_session_token(login_token)
            if session_token:
                cls._token = session_token
                config.set_config("TOKEN", session_token)
            return cls._token

    @classmethod
    def refresh_token(cls):
        with cls._lock:
            login_token = config.get_config("AUTH")
            if not login_token:
                print("[ERROR] No login token (AUTH) found in config for refresh.", file=sys.stderr)
                return None
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
        org_id = None
        role = None
        user_id = None
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], dict):
                d = data["data"]
                session_token = d.get("token")
                org_id = d.get("organization_role_id") or d.get("organization_id")
                role = d.get("role")
                user_id = d.get("user_id")
            elif "token" in data:
                session_token = data["token"]
        if session_token:
            print(f"[INFO] Exchanged login token for session token: {session_token}", file=sys.stderr)
            # Store login token for refresh
            config.set_config("AUTH", login_token)
            # Store org, role, user_id if available
            if org_id:
                config.set_config("ORG", org_id)
            if role:
                config.set_config("ROLE", role)
            if user_id:
                config.set_config("USER_ID", user_id)
            return session_token
        else:
            print(f"[ERROR] Could not extract session token from response: {data}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"[ERROR] Failed to exchange login token for session token: {e}", file=sys.stderr)
        return None

def handle_api_response(response):
    # If 401 or token expired, refresh and retry once
    if response.status_code == 401:
        print("[WARN] Session token expired or invalid, attempting refresh...", file=sys.stderr)
        new_token = SessionTokenCache.refresh_token()
        if new_token:
            return new_token
    return None