"""/write 핸들러 — dry-run + confirm 기반 안전 파일 작성."""

from telegram import Update
from telegram.ext import ContextTypes

from app.services.safety import SafetyError, dry_run_write_file


def _confirmation_message(action):
    return f"{action.preview}\n\nconfirm: /confirm {action.token}\ncancel: /cancel {action.token}"


async def handle_write(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    is_authorized,
    reject_unauthorized,
) -> None:
    if not is_authorized(update):
        await reject_unauthorized(update)
        return
    if not update.message or not update.message.text:
        return

    _, _, body = update.message.text.partition(" ")
    file_path, _, content = body.partition("\n")
    if not file_path.strip() or not content:
        await update.message.reply_text("usage: /write path\\ncontent")
        return

    try:
        action = dry_run_write_file(file_path.strip(), content)
        await update.message.reply_text(_confirmation_message(action))
    except SafetyError as exc:
        await update.message.reply_text(str(exc))
