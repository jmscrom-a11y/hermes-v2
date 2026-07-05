from app.git.backup import backup


def run(prompt: str):
    message = prompt.replace("git", "").replace("백업", "").strip()

    if not message:
        message = "Auto Backup"

    return backup(message)