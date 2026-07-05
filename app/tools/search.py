from duckduckgo_search import DDGS
from app.llm import chat


def run(prompt: str):
    query = (
        prompt.replace("검색", "")
        .replace("검색해", "")
        .replace("찾아", "")
        .strip()
    )

    if not query:
        return "검색어를 입력해주세요."

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    if not results:
        return "검색 결과가 없습니다."

    context = ""

    for i, item in enumerate(results, 1):
        context += f"""
[{i}]
제목: {item['title']}
내용: {item['body']}
링크: {item['href']}
"""

    return chat(
        f"""
다음 검색 결과를 읽고
핵심만 한국어로 요약해줘.

{context}
"""
    )