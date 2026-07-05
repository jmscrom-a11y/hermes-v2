from app.selfedit.engine import self_edit


def run(prompt: str):
    parts = prompt.split(maxsplit=2)

    if len(parts) < 3:
        return (
            "사용법:\n"
            "수정 <파일경로> <요청>\n\n"
            "예)\n"
            "수정 app/telegram_bot.py reply_document로 변경"
        )

    _, path, request = parts

    result = self_edit(path, request)

    diff = result["diff"]

    if len(diff) > 3500:
        diff = diff[:3500] + "\n...(생략)..."

    return (
        f"파일: {path}\n\n"
        f"===== DIFF =====\n"
        f"{diff}\n\n"
        f"적용하려면\n"
        f"apply {path}"
    )