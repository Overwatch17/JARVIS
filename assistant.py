
import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".jarvis"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
