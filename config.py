import os

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL = os.getenv("MODEL", "qwen2.5-coder:14b")

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Agent
BACKUP_DIR = "backup"
LOG_DIR = "logs"
AUTO_RESTART = True
