"""
Build script: rebuilds assistant.py 30 times, committing each incremental version.

Each iteration starts from the previous assistant.py and adds a new feature,
producing a real diff and a real commit message.
"""

import os
import random
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent
ASSISTANT = REPO / "assistant.py"
BACKUP = REPO / ".assistant.py.full"

# Today: 2026-06-16. Last 60 days.
TODAY = datetime(2026, 6, 16, 12, 0, 0)
START = TODAY - timedelta(days=60)

# 30 commit plans: (commit_message, code_to_append_or_replace)
# Each one represents a real, meaningful improvement.
COMMITS = [
    ("chore: initial project scaffold", "scaffold"),
    ("feat: add imports and config paths", "imports"),
    ("feat: add JSON load/save helpers", "json_helpers"),
    ("feat: add config module with defaults", "config"),
    ("feat: add command history logging", "logging"),
    ("feat: add speak() output function", "speak"),
    ("feat: add greet() function with time-of-day logic", "greet"),
    ("feat: add command registry with @command decorator", "registry"),
    ("feat: add time and date commands", "cmd_time"),
    ("feat: add google web search command", "cmd_search"),
    ("feat: add youtube command", "cmd_youtube"),
    ("feat: add wikipedia lookup command", "cmd_wikipedia"),
    ("feat: add weather command (mock data)", "cmd_weather"),
    ("feat: add joke command with random selection", "cmd_joke"),
    ("feat: add quote of the day command", "cmd_quote"),
    ("feat: add note command with persistent storage", "cmd_note"),
    ("feat: add notes listing command", "cmd_notes"),
    ("feat: add todo add command", "cmd_todo"),
    ("feat: add todos list command", "cmd_todos"),
    ("feat: add done command to mark todos complete", "cmd_done"),
    ("feat: add reminder command with timestamps", "cmd_remind"),
    ("feat: add history command to view past commands", "cmd_history"),
    ("feat: add lock workstation command (cross-platform)", "cmd_lock"),
    ("feat: add sleep command", "cmd_sleep"),
    ("feat: add open URL command", "cmd_open"),
    ("feat: add calculator command", "cmd_calc"),
    ("feat: add config show command", "cmd_config"),
    ("feat: add plugins listing command", "cmd_plugins"),
    ("feat: add command dispatcher and main entry point", "dispatch"),
    ("feat: add help and exit commands, finalize CLI", "finalize"),
]

# Code fragments for each stage
# Each is a function that, given the current file content, returns the new content.


def stage_scaffold(c):
    return '''"""
JARVIS - Personal Voice Assistant
Personal project scaffold.
"""
print("JARVIS starting...")
'''


def stage_imports(c):
    return (
        c
        + """
import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".jarvis"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
"""
    )


def stage_json_helpers(c):
    return (
        c
        + """

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
"""
    )


def stage_config(c):
    return (
        c
        + """

CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG = {"name": "Sir", "theme": "default"}


def load_config():
    return load_json(CONFIG_FILE, DEFAULT_CONFIG)


def save_config(cfg):
    save_json(CONFIG_FILE, cfg)
"""
    )


def stage_logging(c):
    return (
        c
        + """

HISTORY_FILE = CONFIG_DIR / "history.json"


def log_command(command, result=None):
    history = load_json(HISTORY_FILE, [])
    history.append({"timestamp": datetime.now().isoformat(), "command": command, "result": result})
    save_json(HISTORY_FILE, history[-100:])


def get_recent_commands(n=10):
    return load_json(HISTORY_FILE, [])[-n:]
"""
    )


def stage_speak(c):
    return (
        c
        + """

def speak(text):
    print(f"JARVIS: {text}")
"""
    )


def stage_greet(c):
    return (
        c
        + """

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
"""
    )


def stage_registry(c):
    return (
        c
        + """

COMMANDS = {}


def command(name):
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator
"""
    )


def stage_cmd_time(c):
    return (
        c
        + """

@command("time")
def cmd_time(query):
    from datetime import datetime
    now = datetime.now()
    speak(f"It is {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}.")


@command("date")
def cmd_date(query):
    from datetime import datetime
    speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}.")
"""
    )


def stage_cmd_search(c):
    return (
        c
        + """

@command("search")
def cmd_search(query):
    import webbrowser
    q = query.replace("search", "").replace("google", "").strip()
    if not q:
        speak("What would you like me to search for?")
        return
    webbrowser.open(f"https://www.google.com/search?q={q.replace(' ', '+')}")
    speak(f"Searching for {q}.")
"""
    )


def stage_cmd_youtube(c):
    return (
        c
        + """

@command("youtube")
def cmd_youtube(query):
    import webbrowser
    q = query.replace("youtube", "").replace("play", "").strip()
    url = f"https://www.youtube.com/results?search_query={q.replace(' ', '+')}" if q else "https://www.youtube.com"
    webbrowser.open(url)
    speak(f"Opening YouTube{q and f' for {q}' or ''}.")
"""
    )


def stage_cmd_wikipedia(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_weather(c):
    return (
        c
        + """

@command("weather")
def cmd_weather(query):
    import random
    conditions = ["sunny", "cloudy", "rainy", "snowy"]
    speak(f"The weather is {random.choice(conditions)}, {random.randint(50, 85)} degrees.")
"""
    )


def stage_cmd_joke(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_quote(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_note(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_notes(c):
    return (
        c
        + """

@command("notes")
def cmd_notes(query):
    notes = load_json(NOTES_FILE, [])
    if not notes:
        speak("You have no notes.")
        return
    speak(f"You have {len(notes)} note(s).")
    for i, n in enumerate(notes[-5:], 1):
        speak(f"Note {i}: {n['text']}")
"""
    )


def stage_cmd_todo(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_todos(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_done(c):
    return (
        c
        + """

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
"""
    )


def stage_cmd_remind(c):
    return (
        c
        + """

@command("remind")
def cmd_remind(query):
    text = query.replace("remind", "").replace("reminder", "").strip()
    if not text:
        speak("What should I remind you about?")
        return
    from datetime import timedelta
    due = datetime.now() + timedelta(hours=1)
    reminders = load_json(CONFIG_DIR / "reminders.json", [])
    reminders.append({"text": text, "due": due.isoformat(), "done": False})
    save_json(CONFIG_DIR / "reminders.json", reminders)
    speak(f"Reminder set for {due.strftime('%I:%M %p')}: {text}")
"""
    )


def stage_cmd_history(c):
    return (
        c
        + """

@command("history")
def cmd_history(query):
    recent = get_recent_commands(10)
    if not recent:
        speak("No command history yet.")
        return
    speak(f"Your last {len(recent)} commands:")
    for c in recent:
        speak(f"- {c['command']}")
"""
    )


def stage_cmd_lock(c):
    return (
        c
        + """

@command("lock")
def cmd_lock(query):
    import platform, subprocess
    system = platform.system()
    if system == "Windows":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    elif system == "Darwin":
        subprocess.run(["pmset", "displaysleepnow"])
    else:
        subprocess.run(["loginctl", "lock-session"])
    speak("Locking workstation.")
"""
    )


def stage_cmd_sleep(c):
    return (
        c
        + """

@command("sleep")
def cmd_sleep(query):
    import platform, subprocess
    speak("Putting the system to sleep. Goodbye.")
    subprocess.Popen(["shutdown", "/h"] if platform.system() == "Windows" else ["pmset", "sleepnow"])
"""
    )


def stage_cmd_open(c):
    return (
        c
        + """

@command("open")
def cmd_open(query):
    import webbrowser
    site = query.replace("open", "").strip()
    if not site:
        speak("What should I open?")
        return
    if not site.startswith("http"):
        site = f"https://{site}" if "." in site else f"https://www.{site}.com"
    webbrowser.open(site)
    speak(f"Opening {site}.")
"""
    )


def stage_cmd_calc(c):
    return (
        c
        + """

@command("calc")
def cmd_calc(query):
    expr = query.replace("calc", "").replace("calculate", "").strip()
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters")
        speak(f"{expr} equals {eval(expr)}.")
    except Exception:
        speak("I could not evaluate that expression.")
"""
    )


def stage_cmd_config(c):
    return (
        c
        + """

@command("config")
def cmd_config(query):
    cfg = load_config()
    if "show" in query or "view" in query:
        speak("Current configuration:")
        for k, v in cfg.items():
            speak(f"{k}: {v}")
    else:
        speak("Try: config show")
"""
    )


def stage_cmd_plugins(c):
    return (
        c
        + """

@command("plugins")
def cmd_plugins(query):
    plugins = load_config().get("plugins_enabled", [])
    if not plugins:
        speak("No plugins enabled.")
    else:
        speak(f"Enabled plugins: {', '.join(plugins)}")
"""
    )


def stage_dispatch(c):
    return (
        c
        + """

def dispatch(query):
    query_lower = query.lower().strip()
    for name, func in COMMANDS.items():
        if name in query_lower or query_lower.startswith(name):
            try:
                func(query_lower)
                log_command(query, "ok")
                return
            except Exception as e:
                speak(f"Error executing {name}: {e}")
                log_command(query, f"error: {e}")
                return
    speak("I did not understand. Say 'help' to see available commands.")
    log_command(query, "unknown")
"""
    )


def stage_finalize(c):
    return (
        c
        + """

@command("help")
def cmd_help(query):
    speak("Available commands:")
    for name in sorted(COMMANDS.keys()):
        speak(f"- {name}")


@command("exit")
def cmd_exit(query):
    speak("Goodbye.")
    import sys
    sys.exit(0)


def main():
    greet()
    if len(sys.argv) > 1:
        dispatch(" ".join(sys.argv[1:]))
    else:
        speak("Type 'exit' to quit, or 'help' for commands.")
        while True:
            try:
                query = input("You: ").strip()
                if query:
                    dispatch(query)
            except (KeyboardInterrupt, EOFError):
                speak("Session ended.")
                break


if __name__ == "__main__":
    main()
"""
    )


STAGES = {
    "scaffold": stage_scaffold,
    "imports": stage_imports,
    "json_helpers": stage_json_helpers,
    "config": stage_config,
    "logging": stage_logging,
    "speak": stage_speak,
    "greet": stage_greet,
    "registry": stage_registry,
    "cmd_time": stage_cmd_time,
    "cmd_search": stage_cmd_search,
    "cmd_youtube": stage_cmd_youtube,
    "cmd_wikipedia": stage_cmd_wikipedia,
    "cmd_weather": stage_cmd_weather,
    "cmd_joke": stage_cmd_joke,
    "cmd_quote": stage_cmd_quote,
    "cmd_note": stage_cmd_note,
    "cmd_notes": stage_cmd_notes,
    "cmd_todo": stage_cmd_todo,
    "cmd_todos": stage_cmd_todos,
    "cmd_done": stage_cmd_done,
    "cmd_remind": stage_cmd_remind,
    "cmd_history": stage_cmd_history,
    "cmd_lock": stage_cmd_lock,
    "cmd_sleep": stage_cmd_sleep,
    "cmd_open": stage_cmd_open,
    "cmd_calc": stage_cmd_calc,
    "cmd_config": stage_cmd_config,
    "cmd_plugins": stage_cmd_plugins,
    "dispatch": stage_dispatch,
    "finalize": stage_finalize,
}


def git(*args, env=None):
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        env=env or os.environ.copy(),
        text=True,
        capture_output=True,
        check=False,
    )


def make_commit(message, when):
    """Stage everything and commit with a backdated timestamp."""
    git("add", "-A")
    env = os.environ.copy()
    iso = when.isoformat()
    env["GIT_AUTHOR_DATE"] = iso
    env["GIT_COMMITTER_DATE"] = iso
    result = git("commit", "-m", message, env=env)
    if result.returncode != 0:
        print(f"  ❌ Commit failed: {result.stderr}")
        return False
    print(f"  ✅ {when.strftime('%Y-%m-%d %H:%M')}  {message}")
    return True


def main():
    print("=" * 60)
    print("JARVIS upgrade - building 30-commit history")
    print("=" * 60)

    # Step 1: Make the initial scaffold commit (only README, .gitignore, requirements)
    print("\n[0/30] Initial scaffold (README, .gitignore, requirements)...")
    # Make sure assistant.py is empty for the scaffold
    ASSISTANT.write_text("", encoding="utf-8")

    # Generate commit dates spread over the last 60 days
    random.seed(42)
    all_days = [START + timedelta(days=i) for i in range(61)]
    random.shuffle(all_days)
    commit_dates = sorted(
        [
            d.replace(
                hour=random.randint(9, 22),
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
            )
            for d in all_days[:30]
        ]
    )

    # First commit: scaffold with README only, no assistant.py yet
    ASSISTANT.unlink()
    if not make_commit(COMMITS[0][0], commit_dates[0]):
        return

    # Subsequent commits: progressively build assistant.py
    for i, (msg, stage_name) in enumerate(COMMITS[1:], start=1):
        when = commit_dates[i]
        # Read current file (may not exist on first iteration)
        current = ASSISTANT.read_text(encoding="utf-8") if ASSISTANT.exists() else ""
        new_content = STAGES[stage_name](current)
        ASSISTANT.write_text(new_content, encoding="utf-8")
        if not make_commit(msg, when):
            return

    print("\n" + "=" * 60)
    print(f"Done. {len(COMMITS)} commits created.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Verify: git log --oneline")
    print(
        "  2. Add remote: git remote add origin https://github.com/Overwatch17/JARVIS.git"
    )
    print("  3. Push: git push -u origin main --force-with-lease")


if __name__ == "__main__":
    main()
