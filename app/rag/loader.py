from pathlib import Path


SUPPORTED_TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
}


def _require_loaders():
    try:
        from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
    except ImportError as exc:
        raise ImportError(
            "RAG loaders require langchain-community and pymupdf. "
            "Install: pip install langchain langchain-community pymupdf"
        ) from exc
    return PyMuPDFLoader, TextLoader


def collect_files(paths, suffixes=None):
    suffixes = suffixes or SUPPORTED_TEXT_SUFFIXES | {".pdf"}
    files = []

    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file() and path.suffix.lower() in suffixes:
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in suffixes:
                    files.append(child)

    return sorted(files)


def load_documents(paths):
    PyMuPDFLoader, TextLoader = _require_loaders()
    documents = []

    for path in collect_files(paths):
        if path.suffix.lower() == ".pdf":
            loader = PyMuPDFLoader(str(path))
        else:
            loader = TextLoader(str(path), encoding="utf-8")
        documents.extend(loader.load())

    return documents
