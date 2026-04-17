# JARVIS — Personal Voice Assistant

A modular Python voice/text assistant inspired by Tony Stark's AI. This is an upgraded, maintainable version of the original basic script.

## Features

- Time, date, weather, jokes, quotes
- Wikipedia & web search
- YouTube launcher
- Notes & persistent todos (JSON storage)
- Reminders with timestamps
- System commands (lock, sleep)
- Simple calculator
- Command history
- Configurable preferences
- Plugin-ready architecture

## Quick start

```bash
pip install -r requirements.txt
python assistant.py                      # interactive mode
python assistant.py time                 # one-shot command
python assistant.py "joke"
python assistant.py "note buy milk"
```

## Configuration

Config and user data live in `~/.jarvis/`:
- `config.json` — name, theme, voice settings
- `notes.json` — your saved notes
- `todos.json` — your todo list
- `history.json` — recent command log

## License

Personal-use. Do whatever you want with it.
