from app.llm import chat


SYSTEM = """
너는 Hermes V2 Code Reviewer이다.

반드시 수정된 코드만 출력한다.

설명하지 않는다.

마크다운(```)을 사용하지 않는다.
"""


def review(source: str, request: str) -> str:
    prompt = f"""
[요청]
{request}

[코드]
{source}
"""

    return chat(
        prompt,
        system=SYSTEM,
    )