from pathlib import Path


def read_file(path: str) -> str:
    file = Path(path)

    if not file.exists():
        raise FileNotFoundError(path)

    return file.read_text(encoding="utf-8")