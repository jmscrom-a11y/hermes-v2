from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from app.core.agent import run
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = run(user_text)
    await update.message.reply_text(reply)


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle)
    )

    print("Hermes V2 Telegram Ready")
    app.run_polling()