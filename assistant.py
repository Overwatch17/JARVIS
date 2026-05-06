
import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".jarvis"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG = {"name": "Sir", "theme": "default"}


def load_config():
    return load_json(CONFIG_FILE, DEFAULT_CONFIG)


def save_config(cfg):
    save_json(CONFIG_FILE, cfg)


HISTORY_FILE = CONFIG_DIR / "history.json"


def log_command(command, result=None):
    history = load_json(HISTORY_FILE, [])
    history.append({"timestamp": datetime.now().isoformat(), "command": command, "result": result})
    save_json(HISTORY_FILE, history[-100:])


def get_recent_commands(n=10):
    return load_json(HISTORY_FILE, [])[-n:]


def speak(text):
    print(f"JARVIS: {text}")


def greet():
    h = datetime.now().hour
    name = load_config().get("name", "Sir")
    if h < 12:
        speak(f"Good morning, {name}.")
    elif h < 18:
        speak(f"Good afternoon, {name}.")
    else:
        speak(f"Good evening, {name}.")
    speak("JARVIS online. How may I assist you?")


COMMANDS = {}


def command(name):
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator
