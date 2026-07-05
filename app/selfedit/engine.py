from app.selfedit.reader import read_file
from app.selfedit.writer import write_file
from app.selfedit.reviewer import review
from app.selfedit.diff import make_diff


def self_edit(path: str, request: str):
    original = read_file(path)

    revised = review(
        original,
        request,
    )

    diff = make_diff(
        original,
        revised,
    )

    return {
        "path": path,
        "original": original,
        "revised": revised,
        "diff": diff,
    }


def apply_edit(path: str, revised: str):
    write_file(
        path,
        revised,
    )

    return True