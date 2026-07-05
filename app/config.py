from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://127.0.0.1:11434/v1"
    )

    OLLAMA_MODEL = os.getenv(
        "OLLAMA_MODEL",
        "qwen3-coder:30b"
    )

settings = Settings()