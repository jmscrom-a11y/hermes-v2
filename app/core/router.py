from app.tools.ppt import run as ppt
from app.tools.search import run as search
from app.tools.git import run as git
from app.tools.self_edit import run as self_edit
from app.llm import chat


def route(prompt: str) -> str:
    text = prompt.lower()

    if "ppt" in text or "발표" in text:
        return ppt(prompt)

    if "검색" in text or "search" in text:
        return search(prompt)

    if "git" in text or "백업" in text:
        return git(prompt)

    if "수정" in text or "edit" in text:
        return self_edit(prompt)

    return chat(prompt)