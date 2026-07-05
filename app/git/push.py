import subprocess


def push():
    subprocess.run(
        ["git", "push"],
        check=True,
    )

    return True