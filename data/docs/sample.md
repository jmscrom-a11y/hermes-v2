# Hermes Agent Documentation

## Overview
Hermes Agent is a Telegram-based AI assistant that uses Retrieval-Augmented Generation (RAG) to answer questions from your documents.

## Architecture
The system consists of three main components:

1. **Telegram Bot** — Receives messages and delivers responses via the Telegram API.
2. **RAG Pipeline** — Loads documents, creates embeddings, and retrieves relevant context for each question.
3. **LLM Integration** — Uses Ollama (nomic-embed-text for embeddings, and a chat model for generation) to generate answers grounded in retrieved documents.

## RAG Pipeline Details
The RAG pipeline works in four stages:

1. **Document Loading** — Reads .md, .py, .txt, .json, .yaml, .pdf files from specified paths.
2. **Chunking** — Splits documents into overlapping chunks (1000 chars, 150 overlap) with metadata (chunk_id, document_id, source, line_range).
3. **Embedding** — Converts chunks to vectors using Ollama's nomic-embed-text model.
4. **Retrieval** — Uses FAISS for vector search, optionally combined with BM25 keyword search via RRF fusion.

## Hybrid Search
When enabled, the pipeline uses HybridRetriever which combines:
- **FAISS cosine similarity** — semantic vector search
- **BM25 keyword search** — exact keyword matching
- **RRF (Reciprocal Rank Fusion)** — merges results from both sources
- **Reranking** — re-scores results using embeddings with a configurable threshold (default 0.35)

## Configuration
Set the following environment variables:
- `BOT_TOKEN` — Telegram bot token
- `OLLAMA_BASE_URL` — Ollama API endpoint (default: http://localhost:11434)
- `OLLAMA_EMBED_MODEL` — Embedding model name (default: nomic-embed-text)
- `RAG_INDEX_DIR` — Path to FAISS index (default: data/faiss_index)
- `RAG_TOP_K` — Number of documents to retrieve (default: 4)

## Safety
The bot includes safety checks for file operations and shell commands, requiring confirmation via /confirm before executing destructive actions.
