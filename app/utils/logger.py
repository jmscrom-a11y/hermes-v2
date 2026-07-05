from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "hermes.log"


def info(message: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] INFO  {message}"

    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def error(message: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ERROR {message}"

    print(line)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")