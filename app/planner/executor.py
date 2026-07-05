from app.planner.planner import plan

from app.llm import chat
from app.tools.search import run as search
from app.tools.ppt import run as ppt
from app.tools.git import run as git
from app.tools.self_edit import run as self_edit


def execute(prompt: str):
    tool = plan(prompt)

    if tool == "search":
        return search(prompt)

    if tool == "ppt":
        return ppt(prompt)

    if tool == "git":
        return git(prompt)

    if tool == "self_edit":
        return self_edit(prompt)

    return chat(prompt)