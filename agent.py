from openai import OpenAI
from config import OLLAMA_BASE_URL, MODEL

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

SYSTEM_PROMPT = """
당신은 Hermes Agent입니다.

역할:
- Python 프로젝트 분석
- 코드 수정 제안
- 버그 수정
- 리팩터링
- 새로운 기능 구현

반드시 기존 코드를 최대한 유지하면서 필요한 부분만 수정하세요.
응답은 수정된 전체 코드만 반환하세요.
"""

def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
