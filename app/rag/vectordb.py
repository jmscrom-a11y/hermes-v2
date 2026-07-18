from pathlib import Path


DEFAULT_INDEX_DIR = "data/faiss_index"


def _require_faiss():
    try:
        from langchain_community.vectorstores import FAISS
    except ImportError as exc:
        raise ImportError(
            "FAISS vector store requires langchain-community and faiss-cpu. "
            "Install: pip install langchain-community faiss-cpu"
        ) from exc
    return FAISS


def create_vector_db(documents, embeddings):
    FAISS = _require_faiss()
    if not documents:
        raise ValueError("Cannot create a FAISS index from an empty document list.")
    return FAISS.from_documents(documents, embeddings)


def save_vector_db(vector_db, index_dir=DEFAULT_INDEX_DIR):
    path = Path(index_dir)
    path.mkdir(parents=True, exist_ok=True)
    vector_db.save_local(str(path))
    return str(path)


def load_vector_db(embeddings, index_dir=DEFAULT_INDEX_DIR):
    FAISS = _require_faiss()
    return FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )
