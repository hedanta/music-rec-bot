from telegram import Update
from telegram.ext import ContextTypes

from app.texts import Texts


async def whoami_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    texts: Texts = context.application.bot_data["texts"]

    user = update.effective_user

    full_name = ""
    username = "—"
    user_id = 0

    if user is not None:
        full_name = user.full_name or ""
        user_id = user.id

        if user.username:
            username = user.username

    message = texts.get(
        "whoami",
        full_name=full_name,
        username=username,
        user_id=user_id,
    )

    await update.message.reply_text(message)
