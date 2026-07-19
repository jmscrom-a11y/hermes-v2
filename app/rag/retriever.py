import math
import re
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from app.rag.vectordb import create_vector_db, load_vector_db, save_vector_db


DEFAULT_TOP_K = 4
DEFAULT_SCORE_THRESHOLD = 0.35


def create_retriever(vector_db, k=DEFAULT_TOP_K, search_type="similarity"):
    return vector_db.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k},
    )


def retrieve_documents(retriever, query):
    if hasattr(retriever, "invoke"):
        return retriever.invoke(query)
    return retriever.get_relevant_documents(query)


# ── BM25 검색기 ──────────────────────────────────────────────


def _tokenize(text: str) -> list[str]:
    """텍스트를 토큰 목록으로 분할 (한글/영문/숫자 모두 지원)."""
    return re.findall(r"[a-zA-Z0-9가-힯ᄀ-ᇿ㄰-㆏ꥠ-꥿ힰ-ힿ]+|[^\s]", text)


@dataclass(frozen=True)
class BM25Retriever:
    """BM25Okapi 기반 키워드 검색기.

    Args:
        documents: 검색할 Document 객체 목록.
    """

    documents: list  # langchain Document objects

    def __post_init__(self):
        tokenized_docs = [_tokenize(doc.page_content) for doc in self.documents]
        object.__setattr__(self, "_tokenized", tokenized_docs)
        object.__setattr__(self, "_bm25", BM25Okapi(tokenized_docs))

    def retrieve(self, query: str, k: int = DEFAULT_TOP_K) -> list:
        """query에 따라 BM25 점수 상위 k개 문서를 반환."""
        if not self.documents:
            return []
        query_tokens = _tokenize(query)
        scores = self._bm25.get_scores(query_tokens)
        top_k_idx = scores.argsort()[::-1][:k]
        return [self.documents[i] for i in top_k_idx]


# ── 임베딩 기반 Reranker ────────────────────────────────────


@dataclass(frozen=True)
class Reranker:
    """Ollama 임베딩 cosine similarity 기반 reranker.

    hybrid 검색 결과에 re-scoring을 적용해 관련도 높은 순으로 정렬하고
    score_threshold 이하 문서를 제거한다.
    """

    threshold: float = DEFAULT_SCORE_THRESHOLD

    def rerank(self, query: str, documents: list, k: int = DEFAULT_TOP_K) -> list:
        """query와 문서 목록에 대해 임베딩 유사도 점수화 → threshold 필터 → 정렬.

        Args:
            query: 검색 쿼리.
            documents: rerank할 Document 목록 (중복 제거 후).
            k: 반환할 최대 문서 수.

        Returns:
            점수 내림차순 정렬된 문서 목록 (threshold 이상만).
        """
        if not documents:
            return []

        from app.rag.embeddings import create_embeddings

        embedder = create_embeddings()
        query_vec = embedder.embed_query(query)

        scored = []
        for item in documents:
            if isinstance(item, tuple):
                doc = item[0]
                content = doc.page_content
            else:
                doc = item
                content = item.page_content
            doc_vec = embedder.embed_documents([content])[0]
            sim = _cosine_similarity(query_vec, doc_vec)
            if sim >= self.threshold:
                scored.append((doc, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _score in scored[:k]]


def _cosine_similarity(a: list, b: list) -> float:
    """두 벡터의 cosine similarity를 계산."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ── Hybrid 검색기 (BM25 + FAISS, RRF fusion + reranking) ────


@dataclass(frozen=True)
class HybridRetriever:
    """FAISS cosine similarity + BM25 키워드 검색을 RRF로 fusion + reranking.

    Args:
        vector_retriever: FAISS retriever (as_retriever() 결과).
        bm25_retriever: BM25Retriever 인스턴스.
        k: 반환할 문서 수.
        reranker: Reranker 인스턴스 (기본값: threshold=0.35).
    """

    vector_retriever: object
    bm25_retriever: BM25Retriever
    k: int = DEFAULT_TOP_K
    reranker: Reranker | None = None

    def retrieve(self, query: str) -> list:
        """RRF fusion → reranking으로 상위 k개 문서를 반환."""
        vector_docs = self._get_vector_results(query)
        bm25_docs = self.bm25_retriever.retrieve(query, k=self.k)

        # 문서 텍스트를 key로 하는 rank mapping
        vector_ranks: dict[str, float] = {}
        for rank, doc in enumerate(vector_docs, start=1):
            vector_ranks[doc.page_content] = 1.0 / rank

        bm25_ranks: dict[str, float] = {}
        for rank, doc in enumerate(bm25_docs, start=1):
            bm25_ranks[doc.page_content] = 1.0 / rank

        # fusion: 모든 candidate에 대해 score 합산
        all_scores: dict[str, float] = {}
        for text, score in vector_ranks.items():
            all_scores[text] = all_scores.get(text, 0.0) + score
        for text, score in bm25_ranks.items():
            all_scores[text] = all_scores.get(text, 0.0) + score

        # doc 객체 매핑
        doc_map: dict[str, object] = {}
        for doc in vector_docs:
            doc_map[doc.page_content] = doc
        for doc in bm25_docs:
            if doc.page_content not in doc_map:
                doc_map[doc.page_content] = doc

        # text -> (doc, rrf_score)
        candidates = [(doc_map[text], score) for text, score in all_scores.items()]

        # reranking 적용 (있는 경우)
        if self.reranker is not None:
            reranked_docs = self.reranker.rerank(query, candidates, k=self.k)
            return reranked_docs

        # reranker 없으면 RRF score 내림차순
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _score in candidates[: self.k]]

    def _get_vector_results(self, query: str) -> list:
        """FAISS retriever 호출 (invoke / get_relevant_documents 호환)."""
        if hasattr(self.vector_retriever, "invoke"):
            return self.vector_retriever.invoke(query)
        return self.vector_retriever.get_relevant_documents(query)

    def get_relevant_documents(self, query: str) -> list:
        """기존 retriever API 호환을 위한 alias."""
        return self.retrieve(query)


def create_hybrid_retriever(vector_retriever, documents, k=DEFAULT_TOP_K, score_threshold=DEFAULT_SCORE_THRESHOLD):
    """FAISS retriever + BM25 retriever를 RRF fusion + reranking으로 결합.

    Args:
        vector_retriever: FAISS.as_retriever() 결과.
        documents: 원본 Document 목록 (BM25 인덱스용).
        k: 반환할 문서 수.
        score_threshold: reranking threshold (기본값 0.35).

    Returns:
        HybridRetriever 인스턴스.
    """
    bm25_retriever = BM25Retriever(documents)
    reranker = Reranker(threshold=score_threshold)
    return HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
        k=k,
        reranker=reranker,
    )
