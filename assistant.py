
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


@command("time")
def cmd_time(query):
    from datetime import datetime
    now = datetime.now()
    speak(f"It is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}.")


@command("date")
def cmd_date(query):
    from datetime import datetime
    speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.")


@command("search")
def cmd_search(query):
    import webbrowser
    q = query.replace("search", "").replace("google", "").strip()
    if not q:
        speak("What would you like me to search for?")
        return
    webbrowser.open(f"https://www.google.com/search?q={q.replace(' ', '+')}")
    speak(f"Searching for {q}.")


@command("youtube")
def cmd_youtube(query):
    import webbrowser
    q = query.replace("youtube", "").replace("play", "").strip()
    url = f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}" if q else "https://www.youtube.com"
    webbrowser.open(url)
    speak(f"Opening YouTube{q and f' for {q}' or ''}.")


@command("wikipedia")
def cmd_wikipedia(query):
    q = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
    if not q:
        speak("What should I look up?")
        return
    try:
        import wikipedia
        speak(f"According to Wikipedia: {wikipedia.summary(q, sentences=2)}")
    except ImportError:
        speak("Install wikipedia: pip install wikipedia")
    except Exception:
        speak(f"I could not find information on {q}.")


@command("weather")
def cmd_weather(query):
    import random
    conditions = ["sunny", "cloudy", "rainy", "snowy"]
    speak(f"The weather is {random.choice(conditions)}, {random.randint(50, 85)} degrees.")


@command("joke")
def cmd_joke(query):
    import random
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the developer go broke? Because he used up all his cache.",
        "There are 10 types of people: those who understand binary and those who don't.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
    ]
    speak(random.choice(jokes))


@command("quote")
def cmd_quote(query):
    import random
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in their dreams. - Eleanor Roosevelt",
    ]
    speak(random.choice(quotes))


NOTES_FILE = CONFIG_DIR / "notes.json"


@command("note")
def cmd_note(query):
    text = query.replace("note", "").replace("remember", "").strip()
    if not text:
        speak("What would you like me to remember?")
        return
    notes = load_json(NOTES_FILE, [])
    notes.append({"timestamp": datetime.now().isoformat(), "text": text})
    save_json(NOTES_FILE, notes)
    speak(f"Noted: {text}")


@command("notes")
def cmd_notes(query):
    notes = load_json(NOTES_FILE, [])
    if not notes:
        speak("You have no notes.")
        return
    speak(f"You have {len(notes)} note(s).")
    for i, n in enumerate(notes[-5:], 1):
        speak(f"Note {i}: {n['text']}")


TODOS_FILE = CONFIG_DIR / "todos.json"


@command("todo")
def cmd_todo(query):
    text = query.replace("todo", "").replace("add", "").strip()
    if not text:
        speak("What should I add to your todo list?")
        return
    todos = load_json(TODOS_FILE, [])
    todos.append({"timestamp": datetime.now().isoformat(), "text": text, "done": False})
    save_json(TODOS_FILE, todos)
    speak(f"Added to your todo list: {text}")


@command("todos")
def cmd_todos(query):
    todos = load_json(TODOS_FILE, [])
    pending = [t for t in todos if not t.get("done")]
    if not pending:
        speak("Your todo list is empty.")
        return
    speak(f"You have {len(pending)} pending task(s).")
    for i, t in enumerate(pending, 1):
        speak(f"{i}. {t['text']}")


@command("done")
def cmd_done(query):
    todos = load_json(TODOS_FILE, [])
    pending = [t for t in todos if not t.get("done")]
    if not pending:
        speak("No pending tasks.")
        return
    try:
        idx = int(query.replace("done", "").strip()) - 1
        if 0 <= idx < len(pending):
            pending[idx]["done"] = True
            save_json(TODOS_FILE, todos)
            speak(f"Marked '{pending[idx]['text']}' as done.")
        else:
            speak("Invalid task number.")
    except ValueError:
        speak("Please specify a task number, e.g., 'done 1'.")
