from app.llm import chat
from app.planner.tools import TOOLS


SYSTEM_PROMPT = f"""
너는 Hermes V2 Planner이다.

사용 가능한 Tool

{TOOLS}

반드시 아래 이름 중 하나만 출력한다.

search
ppt
git
self_edit
chat

설명은 절대 하지 않는다.
"""


def plan(user_prompt: str) -> str:
    tool = chat(
        user_prompt,
        system=SYSTEM_PROMPT,
    ).strip().lower()

    if tool not in {
        "search",
        "ppt",
        "git",
        "self_edit",
        "chat",
    }:
        tool = "chat"

    return tool