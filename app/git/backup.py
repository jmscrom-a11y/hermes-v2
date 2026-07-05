from app.git.commit import commit
from app.git.push import push


def backup(message: str = "Auto Backup"):
    commit(message)
    push()
    return "GitHub 백업 완료"