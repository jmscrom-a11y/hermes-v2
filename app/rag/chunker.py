def _require_splitter():
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError as exc:
        raise ImportError(
            "RAG chunking requires langchain-text-splitters. "
            "Install: pip install langchain-text-splitters"
        ) from exc
    return RecursiveCharacterTextSplitter


def create_text_splitter(chunk_size=1000, chunk_overlap=150):
    RecursiveCharacterTextSplitter = _require_splitter()
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )


def split_documents(documents, chunk_size=1000, chunk_overlap=150):
    splitter = create_text_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)
