import requests
from app.config.settings import OLLAMA_BASE_URL, MODEL

SYSTEM_PROMPT = """
당신은 Hermes Agent입니다.

역할:
- Python 프로젝트 분석
- 코드 수정 제안
- 버그 수정
- 리팩터링
- 새로운 기능 구현

기존 코드를 최대한 유지하면서 필요한 부분만 수정하세요.
"""

def ask_llm(prompt):
    print("=" * 80)
    print("PROMPT SENT TO OLLAMA")
    print(prompt)
    print("=" * 80)

    response = requests.post(
        f"{OLLAMA_BASE_URL.replace('/v1','')}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {
                "num_ctx": 65536
            }
        },
        timeout=600,
    )

    response.raise_for_status()
    return response.json()["message"]["content"]
