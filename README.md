# Hermes Agent

로컬 Ollama LLM과 RAG 파이프라인, Telegram 봇을 연결하는 Python 에이전트 프로젝트입니다.
파일 조작, 셸 실행, 웹 검색 등의 도구를 제공하며, Telegram을 통해 대화형으로 사용할 수 있습니다.

> **상태:** Experimental — API가 안정화되지 않았습니다.

## Quick Start

```bash
# 1. 가상 환경 생성
python3 -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경 변수 설정 (필수)
export OLLAMA_BASE_URL=http://localhost:11434/v1
export MODEL=qwen2.5-coder:14b
export BOT_TOKEN=your_telegram_bot_token   # 봇 사용 시에만 필요

# 4. 봇 실행
python -m app.telegram.bot
```

Ollama가 로컬에서 실행 중이고 해당 모델이 pull되어 있어야 합니다.

## 프로젝트 구조

```text
app/
├── config/
│   └── settings.py          # 환경 기반 설정 (Ollama, Telegram, RAG, 안전성)
├── llm/
│   └── agent.py             # Ollama OpenAI SDK 클라이언트 + ask_llm() 헬퍼
├── prompts/                  # 프롬프트 템플릿 (확장용)
├── rag/
│   ├── chunker.py            # RecursiveCharacterTextSplitter 기반 문서 분할
│   ├── embeddings.py         # Ollama 임베딩 생성
│   ├── loader.py             # 텍스트/PDF 문서 로드 (LangChain + PyMuPDF)
│   ├── pipeline.py           # RAG 파이프라인: build_index, load_pipeline, build_pipeline
│   ├── retriever.py          # FAISS 기반 문서 검색
│   └── vectordb.py           # FAISS 인덱스 생성/저장/로드
├── services/
│   └── safety.py             # dry-run + 확인 기반 안전 파일/셸 연산
├── telegram/
│   ├── bot.py                # Telegram 봇 메인 모듈
│   ├── bot.py.bak            # 이전 버전 백업
│   └── bot_v1.py             # 이전 버전 백업
└── utils/
    └── tools.py              # 파일 백업/읽기/쓰기, 컴파일 체크, 재시작
tests/
├── test_config.py            # 설정 모듈 테스트
├── test_rag_pipeline.py      # RAG 파이프라인 테스트
├── test_safety.py            # 안전성 검증 테스트
├── test_telegram_rag.py      # Telegram RAG 응답 테스트
└── test_tools.py             # 유틸리티 테스트
```

## 모듈

| 모듈 | 설명 |
|------|------|
| `app.config.settings` | 환경 변수 기반 설정. Ollama, Telegram, RAG, 안전성 whitelist 포함 |
| `app.llm.agent` | OpenAI SDK 클라이언트 (Ollama 호환) + `ask_llm()` |
| `app.utils.tools` | 파일 백업, 읽기/쓰기, 컴파일 체크, 재시작 |
| `app.services.safety` | dry-run + 확인 기반 안전 파일/셸 연산 |
| `app.rag.*` | RAG 파이프라인: 문서 로드 → 청킹 → 임베딩 → FAISS → 검색 |
| `app.telegram.bot` | Telegram 봇: RAG 응답, 파일/셸 명령어, 웹 검색, PPT 생성 |

## 환경 변수

### 필수 (Ollama 사용 시)

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama API 엔드포인트 |
| `MODEL` | `qwen2.5-coder:14b` | 사용할 LLM 모델 |

### 필수 (Telegram 봇 사용 시)

| 변수 | 설명 |
|------|------|
| `BOT_TOKEN` | Telegram Bot Token (공백 없이 설정 필요) |

### 선택 (RAG)

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `RAG_INDEX_DIR` | `data/faiss_index` | FAISS 인덱스 저장 경로 |
| `RAG_TOP_K` | `4` | 검색할 문서 수 |
| `OLLAMA_EMBED_MODEL` | `nomic-embed-text` | 임베딩 모델 |
| `OLLAMA_EMBED_BASE_URL` | `http://localhost:11434` | 임베딩용 Ollama URL |

### 선택 (Telegram 안전성)

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `TELEGRAM_ALLOWED_USER_IDS` | (비어있음 = 전체 허용) | 허용된 Telegram 사용자 ID (쉼표 구분) |
| `ALLOWED_FILE_DIRS` | 현재 디렉토리 | 파일 접근 허용 경로 (쉼표 구분) |
| `ALLOWED_SHELL_COMMANDS` | `python3,venv/bin/python,ls,pwd,cat,rg` | 허용된 셸 명령어 (쉼표 구분) |

> **프로덕션:** `TELEGRAM_ALLOWED_USER_IDS`를 반드시 설정하세요. 빈 상태로 두면 모든 사용자가 봇을 이용할 수 있습니다.

## Telegram 명령어

### 메시지 (자동 처리)

일반 텍스트 메시지를 받으면 RAG 파이프라인이 관련 문서를 검색하고 컨텍스트 기반으로 답변합니다.
RAG 인덱스가 없거나 문서가 없으면 LLM이 기본 답변을 생성합니다.

### 보안 명령어

`/write`, `/delete`, `/shell` 명령어는 **dry-run preview → 확인** 절차를 거칩니다.

```
/write path/to/file
content here

/delete path/to/file

/shell ls -la

/confirm <token>     # dry-run 결과를 실제 실행
/cancel <token>      # dry-run 취소
```

모든 파일 연작은 `ALLOWED_FILE_DIRS`로 제한되며, 셸 명령어는 `ALLOWED_SHELL_COMMANDS` whitelist로 필터링됩니다.

### 기타 기능

- **웹 검색:** DuckDuckGo를 통한 뉴스/텍스트 검색
- **PPT 생성:** `python-pptx` 기반 슬라이드 보고서 생성

## 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

RAG 인덱스를 빌드하려면 Ollama에서 임베딩 모델을 미리 pull하세요:

```bash
ollama pull nomic-embed-text
```

## 테스트

```bash
venv/bin/python -m pytest
```

| 테스트 파일 | 내용 |
|------------|------|
| `test_config.py` | 설정 로드 및 파싱 |
| `test_rag_pipeline.py` | RAG 파이프라인 동작 |
| `test_safety.py` | 안전성 검증 (경로/명령어 whitelist) |
| `test_telegram_rag.py` | Telegram RAG 응답 |
| `test_tools.py` | 파일 백업/읽기/쓰기 |

## 코드 검증

```bash
venv/bin/python -m py_compile app/config/settings.py app/llm/agent.py app/utils/tools.py app/telegram/bot.py app/services/safety.py app/rag/pipeline.py app/rag/loader.py app/rag/chunker.py app/rag/embeddings.py app/rag/vectordb.py app/rag/retriever.py
```

## 설정 흐름

```
Telegram 메시지
  -> RAG 인덱스 로드 (RAG_INDEX_DIR)
  -> 관련 문서 검색
  -> 컨텍스트 기반 프롬프트 생성
  -> Ollama LLM 호출 (app.llm.agent.ask_llm)
  -> Telegram 응답
```

RAG 파이프라인 로딩 실패 또는 검색 결과 없음 시, 원본 질문만으로 LLM에 답변을 요청합니다.

## 라이선스

미정
