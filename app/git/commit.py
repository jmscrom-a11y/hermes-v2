import subprocess


def commit(message: str):
    subprocess.run(
        ["git", "add", "."],
        check=True,
    )

    subprocess.run(
        ["git", "commit", "-m", message],
        check=True,
    )

    return True