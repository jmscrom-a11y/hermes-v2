# Hermes Agent Project Analysis Report

작성일: 2026-07-17  
대상 경로: `/Users/crom/hermes-agent`

## 1. 전체 디렉터리 트리

`venv/lib/python3.14/site-packages` 내부까지 실제 파일은 5,700개 이상이며 대부분 외부 패키지입니다. 아래 트리는 프로젝트 소유 파일과 하위 디렉터리 구조를 중심으로 정리했습니다.

```text
hermes-agent/
├── .git/
│   └── Git 저장소 메타데이터
├── __pycache__/
│   ├── agent.cpython-314.pyc
│   ├── config.cpython-314.pyc
│   └── tools.cpython-314.pyc
├── venv/
│   ├── .gitignore
│   ├── pyvenv.cfg
│   ├── bin/
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── Activate.ps1
│   │   ├── ddgs
│   │   ├── distro
│   │   ├── dotenv
│   │   ├── httpx
│   │   ├── idna
│   │   ├── normalizer
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.14
│   │   ├── tqdm
│   │   ├── vba_extract.py
│   │   └── watchmedo
│   ├── include/
│   └── lib/
│       └── python3.14/
│           └── site-packages/
│               ├── openai/
│               ├── telegram/
│               ├── duckduckgo_search/
│               ├── pptx/
│               ├── requests/
│               ├── httpx/
│               ├── pydantic/
│               ├── GitPython 관련 패키지
│               ├── watchdog 관련 패키지
│               ├── pillow/PIL 관련 패키지
│               └── 기타 설치 의존성
├── agent.py
├── agent.pyecho
├── config.py
├── report.md
├── report.pptx
├── tg_bot.py
├── tg_bot.py.bak
├── tg_bot_v1.py
└── tools.py
```

용량 기준:

- 전체 프로젝트: 약 `109M`
- `venv/`: 약 `109M`
- `.git/`: 약 `152K`
- `__pycache__/`: 약 `12K`
- `report.pptx`: 약 `28K`

현재 Git 추적 파일:

```text
agent.py
agent.pyecho
config.py
report.pptx
tg_bot.py
tg_bot.py.bak
tg_bot_v1.py
tools.py
```

## 2. 각 파일의 역할

| 파일/디렉터리 | 역할 | 상태 |
|---|---|---|
| `agent.py` | OpenAI Python SDK를 Ollama OpenAI 호환 엔드포인트에 연결하고 `ask_llm(prompt)`로 채팅 완성 요청을 보내는 LLM 래퍼 | 문법 정상, 기능은 최소 수준 |
| `config.py` | `OLLAMA_BASE_URL`, `MODEL`, `BOT_TOKEN`, 백업/로그/자동 재시작 설정 정의 | 문법 정상, 설정 검증 없음 |
| `tools.py` | 파일 백업, 파일 읽기/쓰기, `py_compile` 검사, `restart.sh` 실행 함수 제공 | 문법 정상, 안전장치 부족 |
| `tg_bot.py` | Telegram 봇 엔트리로 보임. Telegram, DuckDuckGo, PPT 생성, Ollama URL 상수 일부 포함 | 문법 오류로 실행 불가 |
| `tg_bot_v1.py` | `tg_bot.py`와 동일한 버전 복사본 | 문법 오류로 실행 불가 |
| `tg_bot.py.bak` | `tg_bot.py`와 동일한 백업 파일 | 문법 오류로 실행 불가, 복구 기준으로 부적합 |
| `agent.pyecho` | `msg.append(...)` 코드 조각이 한 줄로 남은 파일 | 깨진 임시 산출물로 보임 |
| `report.pptx` | `tg_bot.py`의 `make_ppt()`가 생성한 것으로 보이는 PPT 산출물 | 소스 코드 아님 |
| `__pycache__/` | Python 바이트코드 캐시 | 생성 산출물 |
| `venv/` | Python 3.14 가상환경과 설치 패키지 | 재현 가능한 의존성 파일은 없음 |
| `.git/` | Git 저장소 메타데이터 | 정상 |
| `report.md` | 본 분석 보고서 | 신규 분석 산출물 |

## 3. 현재 구현된 기능

현재 구현되어 실제로 확인 가능한 기능은 다음 정도입니다.

### LLM 호출

`agent.py`:

- `OpenAI` 클라이언트를 생성합니다.
- 기본 base URL은 `http://localhost:11434/v1`입니다.
- 기본 모델은 `qwen2.5-coder:14b`입니다.
- `ask_llm(prompt)` 함수가 system/user 메시지를 구성해 `client.chat.completions.create()`를 호출합니다.
- temperature는 `0.2`로 고정되어 있습니다.

### 설정 로딩

`config.py`:

- 환경변수 `OLLAMA_BASE_URL`, `MODEL`, `BOT_TOKEN`을 읽습니다.
- 기본 백업 디렉터리는 `backup`입니다.
- 기본 로그 디렉터리는 `logs`입니다.
- `AUTO_RESTART = True`가 정의되어 있습니다.

### 파일 유틸리티

`tools.py`:

- `backup_file(file_path)`: 대상 파일이 존재하면 `backup/파일명.타임스탬프.bak`로 복사합니다.
- `read_file(file_path)`: UTF-8 텍스트 파일을 읽습니다.
- `write_file(file_path, content)`: 백업 후 UTF-8로 파일을 씁니다.
- `compile_check(file_path)`: `python3 -m py_compile`로 문법 검사를 수행합니다.
- `restart()`: `bash restart.sh`를 비동기로 실행합니다.

### Telegram/PPT/Web Search 의도

`tg_bot.py` 계열:

- `telegram` 패키지의 `Update`, `Application`, `MessageHandler`, `filters`를 import합니다.
- `duckduckgo_search.DDGS`를 import합니다.
- `pptx.Presentation()`으로 `report.pptx`를 생성하는 `make_ppt(t, c)` 함수가 있습니다.
- `DDGS().news()` 및 `DDGS().text()`로 웹 검색을 수행하려는 `search_web(q)` 함수 일부가 있습니다.

단, `tg_bot.py`가 16번째 줄에서 끊겨 있어 Telegram 봇 기능은 현재 실행 가능한 구현으로 볼 수 없습니다.

## 4. 구현되지 않은 기능

다음 기능은 코드상 의도만 있거나 아예 없습니다.

- Telegram 봇 실행 엔트리포인트
- Telegram 메시지 핸들러
- Telegram `BOT_TOKEN` 검증
- 사용자 메시지를 LLM으로 전달하는 봇 플로우
- Ollama 호출 실패 처리
- 웹 검색 결과 반환/요약
- PPT 생성 결과를 Telegram으로 전송
- 파일 수정 명령 처리
- 파일 수정 전 사용자 승인
- 프로젝트 전체 코드 분석 기능
- 대화 메모리
- 세션별 상태 관리
- 로그 기록
- `logs/` 디렉터리 사용
- 자동 재시작 루프
- `restart.sh`
- 테스트
- 의존성 명세 파일
- README/운영 문서
- RAG 파이프라인
- 문서/코드 인덱싱
- 임베딩 생성
- 벡터 검색
- Retriever
- source citation
- 권한/보안 모델

## 5. RAG 구현 상태

현재 RAG는 구현되어 있지 않습니다. 항목별 상태는 다음과 같습니다.

| 구성요소 | 현재 상태 | 근거 |
|---|---|---|
| Loader | 없음 | 파일, PDF, 웹, Git 저장소, Telegram 첨부 등을 로딩하는 코드가 없음 |
| Chunker | 없음 | 텍스트 분할, overlap, token budget 관리 코드가 없음 |
| Embedding | 없음 | embedding API 호출 또는 로컬 embedding 모델 호출 코드가 없음 |
| Vector DB | 없음 | Chroma, FAISS, Qdrant, Milvus, Weaviate 등 사용 코드/의존성 없음 |
| Retriever | 없음 | similarity search, keyword search, hybrid search, reranking 코드 없음 |
| Prompt | 부분 존재 | `agent.py`의 `SYSTEM_PROMPT`만 존재. 검색 컨텍스트 주입 프롬프트는 없음 |
| Metadata | 없음 | 문서 ID, 파일 경로, 라인 번호, chunk ID, score 저장 구조 없음 |
| Citation | 없음 | 답변에 출처를 붙이는 구조 없음 |
| Index Refresh | 없음 | 파일 변경 감지, 재색인, incremental indexing 없음 |

현재 `agent.py`의 `ask_llm(prompt)`는 사용자의 프롬프트를 그대로 모델에 전달합니다. 즉, “질문 → 검색 → 관련 컨텍스트 구성 → LLM 답변” 흐름이 아니라 “질문 → LLM 답변” 흐름입니다.

설치된 패키지에도 RAG 전용 의존성은 보이지 않습니다. `openai` 패키지 내부에 `vector_stores` 리소스 모듈은 포함되어 있지만, 이 프로젝트 코드에서 사용하지 않습니다.

## 6. 텔레그램 봇 구조

현재 Telegram 봇 구조는 미완성입니다.

`tg_bot.py`, `tg_bot_v1.py`, `tg_bot.py.bak`는 모두 동일한 16줄 파일이며 다음 요소만 있습니다.

- import:
  - `os`
  - `json`
  - `requests`
  - `pptx`
  - `telegram.Update`
  - `telegram.ext.Application`
  - `telegram.ext.MessageHandler`
  - `telegram.ext.filters`
  - `duckduckgo_search.DDGS`
- 상수:
  - `URL = "http://localhost:11434/v1/chat/completions"`
- 함수:
  - `make_ppt(t, c)`
  - `search_web(q)` 일부

없는 요소:

- `BOT_TOKEN` import 또는 사용
- `Application.builder().token(...).build()`
- message handler 등록
- async handler 함수
- `run_polling()` 또는 webhook 실행
- 명령어 라우팅
- 에러 핸들러
- Ollama 요청 payload 구성
- 응답 전송
- PPT 파일 전송
- 사용자 인증/허용 목록

현재 상태에서는 Telegram 봇은 시작조차 할 수 없습니다.

## 7. Ollama 연동 구조

Ollama 연동은 두 군데에 흔적이 있습니다.

### `agent.py`

```python
client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)
```

- OpenAI Python SDK를 사용합니다.
- `base_url`을 Ollama의 OpenAI 호환 API 주소로 바꿉니다.
- API key는 Ollama에서 실질적으로 의미 없는 `"ollama"` 고정 문자열입니다.
- `chat.completions.create()`를 호출합니다.

### `config.py`

```python
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL = os.getenv("MODEL", "qwen2.5-coder:14b")
```

- 환경변수로 base URL과 model을 바꿀 수 있습니다.
- 기본값은 로컬 Ollama를 전제로 합니다.

### `tg_bot.py`

```python
URL = "http://localhost:11434/v1/chat/completions"
```

- 직접 HTTP 호출을 하려는 흔적입니다.
- 하지만 실제 `requests.post()` 호출은 없습니다.
- `agent.py`의 OpenAI SDK 방식과 `tg_bot.py`의 raw HTTP 방식이 분리되어 있어 설계가 일관되지 않습니다.

문제점:

- timeout 없음
- retry 없음
- 모델 존재 여부 확인 없음
- Ollama 서버 상태 확인 없음
- streaming 없음
- 에러 메시지 정규화 없음
- Telegram 봇과 `agent.py`가 연결되어 있지 않음

## 8. 발견된 버그 목록

### B1. `tg_bot.py` 문법 오류

`tg_bot.py` 13~16줄:

```python
def search_web(q):
    try:
        res = DDGS().news(q, max_results=5)
        if not res: res = DDGS().text(q, max_results=5)
```

`try` 블록에 `except` 또는 `finally`가 없어 `SyntaxError`가 발생합니다.

검증 결과:

```text
File "tg_bot.py", line 16
  if not res: res = DDGS().text(q, max_results=5)
                                                 ^
SyntaxError: expected 'except' or 'finally' block
```

### B2. `tg_bot_v1.py`, `tg_bot.py.bak`도 동일하게 깨짐

복구용 백업처럼 보이는 파일들이 모두 같은 16줄 미완성 코드입니다. 실제 복구 기준으로 쓸 수 없습니다.

### B3. Telegram 봇 엔트리포인트 부재

`Application`, `MessageHandler`, `filters`를 import하지만 handler 등록 및 실행 코드가 없습니다.

### B4. `BOT_TOKEN` 미검증

`config.py`에서 `BOT_TOKEN` 기본값이 빈 문자열입니다. 실행 시 토큰 누락을 조기에 감지하는 코드가 없습니다.

### B5. `restart.sh` 부재

`tools.py`의 `restart()`는 `bash restart.sh`를 실행하지만 루트에 `restart.sh`가 없습니다.

### B6. 파일 쓰기 기능의 경로 제한 없음

`tools.py`의 `write_file(file_path, content)`는 전달받은 경로에 그대로 씁니다. Telegram 봇과 연결될 경우 임의 파일 수정 위험이 큽니다.

### B7. 백업 디렉터리와 로그 디렉터리의 운영 정책 없음

`BACKUP_DIR`, `LOG_DIR`는 정의되어 있지만 로그 기능은 없고 백업 보존 정책도 없습니다.

### B8. `agent.py` 시스템 프롬프트가 사용 목적과 충돌

`SYSTEM_PROMPT`가 “응답은 수정된 전체 코드만 반환하세요”를 강제합니다. 분석, 설명, RAG 답변, Telegram 일반 대화에는 부적합합니다.

### B9. 예외 처리 없음

`agent.py`, `tools.py`, `tg_bot.py` 모두 네트워크 오류, 파일 IO 오류, 모델 오류, 권한 오류를 사용자 친화적으로 처리하지 않습니다.

### B10. 의존성 재현 불가

`requirements.txt` 또는 `pyproject.toml`이 없습니다. 현재 설치 패키지는 `venv`에만 존재합니다.

### B11. 가상환경이 프로젝트 내부에 있음

`venv/`가 프로젝트 내부에 있어 용량 대부분을 차지합니다. 현재 Git에는 추적되지 않지만, `.gitignore`가 루트에 없어 실수로 포함될 위험이 있습니다.

### B12. `agent.pyecho`가 깨진 산출물

`agent.pyecho`는 한 줄짜리 깨진 코드 조각입니다. 실행 가능한 Python 파일도 아니고 문서도 아닙니다.

### B13. 중복 파일 관리 문제

`tg_bot.py`, `tg_bot_v1.py`, `tg_bot.py.bak`가 동일 내용입니다. 어떤 파일이 canonical source인지 불명확합니다.

## 9. Hermes V3 수준으로 개선하려면 필요한 작업

### P0. 실행 가능 상태 복구

1. `tg_bot.py` 문법 오류 수정
2. Telegram 봇 엔트리포인트 구현
3. `BOT_TOKEN` 누락 시 명확히 실패하도록 설정 검증 추가
4. `tg_bot_v1.py`, `tg_bot.py.bak`, `agent.pyecho` 정리 방침 결정
5. `restart.sh`를 만들거나 `restart()` 제거/비활성화

### P1. 프로젝트 기본 골격 정리

1. `requirements.txt` 또는 `pyproject.toml` 생성
2. 루트 `.gitignore` 추가
3. `README.md` 작성
4. 실행 명령, 환경변수, Ollama 모델 준비 절차 문서화
5. 소스 디렉터리 구조 도입
   - 예: `hermes/agent.py`, `hermes/bot.py`, `hermes/rag/`, `hermes/tools/`

### P2. Ollama/LLM 계층 정리

1. `agent.py`를 단일 LLM gateway로 정리
2. raw `requests` 방식과 OpenAI SDK 방식 중 하나로 통일
3. timeout, retry, error handling 추가
4. 모델 설정 검증 추가
5. 시스템 프롬프트를 작업 유형별로 분리
   - 일반 답변
   - 코드 분석
   - 코드 수정 제안
   - RAG 답변
   - Telegram 짧은 응답

### P3. Telegram 봇 아키텍처 구현

1. async message handler 구현
2. 명령어 라우팅 추가
   - `/ask`
   - `/search`
   - `/rag`
   - `/ppt`
   - `/status`
3. 사용자별 세션 상태 관리
4. 긴 답변 분할 전송
5. 오류 메시지 표준화
6. 파일 전송 기능 구현
7. 관리자/허용 사용자 제한

### P4. RAG V1 구현

1. Loader 추가
   - 코드 파일 로더
   - Markdown/text 로더
   - PDF/PPTX 로더는 필요 시 추가
2. Chunker 추가
   - 파일 경로, 라인 범위, chunk ID 메타데이터 포함
3. Embedding 추가
   - Ollama embedding 모델 또는 OpenAI-compatible embedding API
4. Vector DB 추가
   - 로컬 우선이면 Chroma 또는 FAISS
   - 운영 확장성이 필요하면 Qdrant
5. Retriever 추가
   - top-k similarity search
   - 파일 경로 필터
   - score threshold
6. Prompt builder 추가
   - 검색 컨텍스트
   - 출처
   - 답변 규칙
7. Citation 추가
   - 파일 경로와 라인 범위 표시

### P5. RAG V2 품질 개선

1. Hybrid search 추가
   - BM25 + vector search
2. Reranker 추가
3. incremental indexing
4. 파일 변경 감지
5. chunk 중복 제거
6. context budget 관리
7. 답변 평가용 테스트셋 작성

### P6. 안전한 코드 수정 에이전트화

1. 파일 쓰기 allowlist
2. dry-run diff 생성
3. 사용자 승인 후 적용
4. 자동 백업과 rollback
5. compile/test 검증
6. destructive command 차단

### P7. 운영성 강화

1. structured logging
2. health check
3. status command
4. graceful shutdown
5. config schema
6. 테스트 자동화
7. CI 도입

## 결론

현재 프로젝트는 Hermes V3라고 보기 어렵고, “Ollama LLM 호출 래퍼 + 미완성 Telegram 봇 조각 + 일부 파일 유틸리티” 단계입니다. 특히 RAG는 구성요소가 전혀 구현되어 있지 않습니다.

가장 먼저 해야 할 일은 `tg_bot.py` 실행 가능 상태 복구와 프로젝트 골격 정리입니다. 그다음 LLM gateway를 안정화하고, 별도 `rag/` 모듈로 Loader, Chunker, Embedding, Vector DB, Retriever, Prompt Builder를 순서대로 추가하는 방식이 적절합니다.
