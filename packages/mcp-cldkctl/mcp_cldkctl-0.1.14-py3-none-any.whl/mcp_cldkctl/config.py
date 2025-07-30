import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".cldkctl"
CONFIG_FILE = CONFIG_DIR / "config.json"

_config_cache = None

def load_config():
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            _config_cache = json.load(f)
    else:
        _config_cache = {}
    return _config_cache

def save_config():
    global _config_cache
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(_config_cache or {}, f, indent=2)

def get_config(key, default=None):
    cfg = load_config()
    return cfg.get(key, default)

def set_config(key, value):
    cfg = load_config()
    cfg[key] = value
    save_config() 