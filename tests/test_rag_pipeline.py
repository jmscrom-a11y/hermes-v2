from dataclasses import dataclass
import unittest

from langchain_core.embeddings import Embeddings

from app.rag.pipeline import PromptBuilder, RAGPipeline
from app.rag.retriever import create_retriever, retrieve_documents
from app.rag.vectordb import create_vector_db


@dataclass
class FakeDocument:
    page_content: str
    metadata: dict


class FakeRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.last_query = None

    def invoke(self, query):
        self.last_query = query
        return self.documents


class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        lowered = text.lower()
        return [
            float(lowered.count("faiss")),
            float(lowered.count("ollama")),
            0.0,
        ]


class RAGPipelineTest(unittest.TestCase):
    def test_prompt_builder_includes_question_context_and_source(self):
        documents = [
            FakeDocument(
                page_content="Hermes uses FAISS for vector search.",
                metadata={"source": "docs/rag.md", "page": 1},
            )
        ]

        prompt = PromptBuilder().build("What does Hermes use?", documents)

        self.assertIn("What does Hermes use?", prompt)
        self.assertIn("Hermes uses FAISS for vector search.", prompt)
        self.assertIn("docs/rag.md:1", prompt)

    def test_rag_pipeline_retrieves_builds_prompt_and_calls_llm(self):
        documents = [
            FakeDocument(
                page_content="Ollama embeddings are used.",
                metadata={"source": "docs/rag.md"},
            )
        ]
        retriever = FakeRetriever(documents)
        seen_prompts = []

        def fake_llm(prompt):
            seen_prompts.append(prompt)
            return "answer"

        pipeline = RAGPipeline(retriever=retriever, llm=fake_llm)

        result = pipeline.answer("Which embeddings are used?")

        self.assertEqual("answer", result)
        self.assertEqual("Which embeddings are used?", retriever.last_query)
        self.assertIn("Ollama embeddings are used.", seen_prompts[0])

    def test_faiss_vector_db_and_retriever_return_documents(self):
        from langchain_core.documents import Document

        documents = [
            Document(page_content="FAISS stores vectors.", metadata={"source": "a.md"}),
            Document(page_content="Ollama creates embeddings.", metadata={"source": "b.md"}),
        ]

        vector_db = create_vector_db(documents, FakeEmbeddings())
        retriever = create_retriever(vector_db, k=1)
        results = retrieve_documents(retriever, "FAISS")

        self.assertEqual(1, len(results))
        self.assertIn("FAISS", results[0].page_content)


if __name__ == "__main__":
    unittest.main()
