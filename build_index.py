"""Build and persist a FAISS index from documents in data/docs."""

import os
import pathlib

from app.config.settings import OLLAMA_BASE_URL
from app.rag.embeddings import DEFAULT_EMBEDDING_MODEL
from app.rag.pipeline import build_index

ROOT = pathlib.Path(__file__).resolve().parent
DOCS_DIR = ROOT / "data" / "docs"
INDEX_DIR = ROOT / "data" / "faiss_index"


def main() -> None:
    # Resolve embedding model from .env (via pydantic-settings / os.environ)
    embed_model = os.getenv("OLLAMA_EMBED_MODEL", DEFAULT_EMBEDDING_MODEL)

    # Ollama base URL for embeddings (strip /v1 suffix if present)
    base_url = os.getenv("OLLAMA_EMBED_BASE_URL", OLLAMA_BASE_URL.removesuffix("/v1"))

    # Load all files under data/docs
    paths = [str(p) for p in DOCS_DIR.rglob("*") if p.is_file()]
    if not paths:
        print(f"No documents found under {DOCS_DIR}")
        return

    # Build and persist the index
    build_index(
        paths=paths,
        index_dir=str(INDEX_DIR),
        embedding_model=embed_model,
    )

    print("Index build completed.")


if __name__ == "__main__":
    main()
