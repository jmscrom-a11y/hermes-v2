import os

from app.config.settings import OLLAMA_BASE_URL


DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"


def _ollama_native_base_url():
    return os.getenv(
        "OLLAMA_EMBED_BASE_URL",
        OLLAMA_BASE_URL.removesuffix("/v1"),
    )


def create_embeddings(model=None, base_url=None):
    try:
        from langchain_ollama import OllamaEmbeddings
    except ImportError as exc:
        raise ImportError(
            "Ollama embeddings require langchain-ollama. "
            "Install: pip install langchain-ollama"
        ) from exc

    return OllamaEmbeddings(
        model=model or os.getenv("OLLAMA_EMBED_MODEL", DEFAULT_EMBEDDING_MODEL),
        base_url=base_url or _ollama_native_base_url(),
    )
