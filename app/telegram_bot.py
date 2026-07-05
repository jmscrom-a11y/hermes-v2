from pathlib import Path
import os

from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.core.agent import run

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"[Telegram] {user_text}")

    reply = run(user_text)

    if isinstance(reply, str) and reply.endswith(".pptx"):
        with open(reply, "rb") as f:
            await update.message.reply_document(document=f)
        return

    await update.message.reply_text(str(reply))


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle,
        )
    )

    print("Hermes V2 Telegram Ready")

    app.run_polling()