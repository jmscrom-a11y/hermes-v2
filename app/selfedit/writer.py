from pathlib import Path


def write_file(path: str, content: str):
    file = Path(path)

    file.parent.mkdir(parents=True, exist_ok=True)

    file.write_text(
        content,
        encoding="utf-8",
    )