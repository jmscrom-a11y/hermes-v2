from app.utils.logger import info, error
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

    info(f"Telegram <- {user_text}")

    try:
        reply = run(user_text)

        if isinstance(reply, str) and reply.endswith(".pptx"):
            with open(reply, "rb") as f:
                await update.message.reply_document(document=f)

            info(f"PPT -> {reply}")
            return

        await update.message.reply_text(str(reply))
        info("Reply sent")

    except Exception as e:
        error(str(e))
        await update.message.reply_text(
            f"오류가 발생했습니다.\n{e}"
        )


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