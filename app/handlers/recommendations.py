from telegram import Update
from telegram.ext import ContextTypes

from app.texts import Texts


async def getrecommendation_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.message is None:
        return

    texts: Texts = context.application.bot_data["texts"]

    message = texts.get("getrecommendation_stub")
    await update.message.reply_text(message)


async def myrecommendations_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.message is None:
        return

    texts: Texts = context.application.bot_data["texts"]

    message = texts.get("myrecommendations_stub")
    await update.message.reply_text(message)
