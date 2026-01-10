from telegram import Update
from telegram.ext import ContextTypes

from app.texts import Texts


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    texts: Texts = context.application.bot_data["texts"]

    message = texts.get("start")
    await update.message.reply_text(message)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    texts: Texts = context.application.bot_data["texts"]

    message = texts.get("help")
    await update.message.reply_text(message)
