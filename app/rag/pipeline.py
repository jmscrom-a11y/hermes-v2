from dataclasses import dataclass

from app.llm.agent import ask_llm
from app.rag.chunker import split_documents
from app.rag.embeddings import create_embeddings
from app.rag.loader import load_documents
from app.rag.retriever import (
    BM25Retriever,
    HybridRetriever,
    create_hybrid_retriever,
    create_retriever,
    retrieve_documents,
)
from app.rag.vectordb import create_vector_db, load_vector_db, save_vector_db


DEFAULT_RAG_TEMPLATE = """당신은 Hermes Agent의 RAG 응답 엔진입니다.
아래 컨텍스트만 근거로 사용해 한국어로 답변하세요.
컨텍스트에 답이 없으면 모른다고 말하세요.

질문:
{question}

컨텍스트:
{context}

답변:"""


def _require_prompt_template():
    try:
        from langchain_core.prompts import PromptTemplate
    except ImportError:
        class PromptTemplate:
            def __init__(self, template, input_variables):
                self.template = template
                self.input_variables = input_variables

            def format(self, **kwargs):
                return self.template.format(**kwargs)

    return PromptTemplate


@dataclass
class PromptBuilder:
    template: str = DEFAULT_RAG_TEMPLATE

    def __post_init__(self):
        PromptTemplate = _require_prompt_template()
        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["question", "context"],
        )

    def build_context(self, documents):
        parts = []
        for index, document in enumerate(documents, start=1):
            metadata = getattr(document, "metadata", {}) or {}
            source = metadata.get("source", "unknown")
            page = metadata.get("page")
            location = f"{source}:{page}" if page is not None else source
            content = getattr(document, "page_content", str(document))
            parts.append(f"[{index}] {location}\n{content}")
        return "\n\n".join(parts)

    def build(self, question, documents):
        return self.prompt.format(
            question=question,
            context=self.build_context(documents),
        )


class RAGPipeline:
    def __init__(self, retriever, llm=ask_llm, prompt_builder=None, hybrid=False, documents=None):
        self.llm = llm
        self.prompt_builder = prompt_builder or PromptBuilder()

        if hybrid and documents is not None:
            self.retriever = create_hybrid_retriever(retriever, documents)
        else:
            self.retriever = retriever

    def retrieve(self, question):
        return retrieve_documents(self.retriever, question)

    def build_prompt(self, question, documents=None):
        documents = documents if documents is not None else self.retrieve(question)
        return self.prompt_builder.build(question, documents)

    def answer(self, question):
        documents = self.retrieve(question)
        prompt = self.prompt_builder.build(question, documents)
        answer = self.llm(prompt)
        return self._format_answer(answer, documents)

    def _format_answer(self, answer, documents):
        """답변에 Sources 섹션을 붙여 반환."""
        if not documents:
            return answer

        sources = []
        for doc in documents:
            metadata = getattr(doc, "metadata", {}) or {}
            source = metadata.get("source", "unknown")
            line_range = metadata.get("line_range")
            if line_range:
                sources.append(f"- {source} (lines {line_range[0]}-{line_range[1]})")
            else:
                sources.append(f"- {source}")

        return f"{answer}\n\nSources:\n" + "\n".join(sources)


def build_index(paths, index_dir=None, embedding_model=None, chunk_size=1000, chunk_overlap=150):
    documents = load_documents(paths)
    chunks = split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    embeddings = create_embeddings(model=embedding_model)
    vector_db = create_vector_db(chunks, embeddings)
    if index_dir:
        save_vector_db(vector_db, index_dir)
    return vector_db


def load_pipeline(index_dir, embedding_model=None, k=4, llm=ask_llm, hybrid=False, documents=None, score_threshold=0.35):
    embeddings = create_embeddings(model=embedding_model)
    vector_db = load_vector_db(embeddings, index_dir)
    retriever = create_retriever(vector_db, k=k)
    if hybrid and documents is not None:
        pipeline_retriever = create_hybrid_retriever(retriever, documents, score_threshold=score_threshold)
    else:
        pipeline_retriever = retriever
    return RAGPipeline(retriever=pipeline_retriever, llm=llm)


def build_pipeline(paths, index_dir=None, embedding_model=None, k=4, llm=ask_llm, hybrid=False, score_threshold=0.35):
    docs = load_documents(paths)
    chunks = split_documents(
        docs,
        chunk_size=1000,
        chunk_overlap=150,
    )
    embeddings = create_embeddings(model=embedding_model)
    vector_db = create_vector_db(chunks, embeddings)
    retriever = create_retriever(vector_db, k=k)
    if hybrid:
        pipeline_retriever = create_hybrid_retriever(retriever, docs, score_threshold=score_threshold)
    else:
        pipeline_retriever = retriever
    return RAGPipeline(retriever=pipeline_retriever, llm=llm)
