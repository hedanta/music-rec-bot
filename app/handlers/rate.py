import re

from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import ContextTypes

from app.texts import Texts

TRACK_RE = re.compile(r"^\s*(?P<artist>.+?)\s*-\s*(?P<title>.+?)\s*$")

CALLBACK_PREFIX = "rate:"


def _build_rate_keyboard(artist: str, title: str) -> InlineKeyboardMarkup:
    payload_base = f"{CALLBACK_PREFIX}{artist}|{title}|"

    keyboard = [
        [
            InlineKeyboardButton("👍 Like", callback_data=payload_base + "like"),
            InlineKeyboardButton("😐 Neutral", callback_data=payload_base + "neutral"),
            InlineKeyboardButton("👎 Dislike", callback_data=payload_base + "dislike"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def rate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    texts: Texts = context.application.bot_data["texts"]

    raw_text = update.message.text or ""
    parts = raw_text.split(" ", 1)

    if len(parts) < 2:
        await update.message.reply_text(texts.get("rate_usage"))
        return

    payload = parts[1]
    match = TRACK_RE.match(payload)

    if match is None:
        await update.message.reply_text(texts.get("rate_usage"))
        return

    artist = match.group("artist").strip()
    title = match.group("title").strip()

    keyboard = _build_rate_keyboard(artist=artist, title=title)

    message = texts.get("rate_choose", artist=artist, title=title)
    await update.message.reply_text(message, reply_markup=keyboard)


async def rate_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if update.callback_query is None:
        return

    texts: Texts = context.application.bot_data["texts"]
    query = update.callback_query

    data = query.data or ""
    if not data.startswith(CALLBACK_PREFIX):
        return

    await query.answer()

    payload = data[len(CALLBACK_PREFIX) :]

    # Ожидаем формат: artist|title|value
    parts = payload.split("|")
    if len(parts) != 3:
        await query.edit_message_text(texts.get("error_generic"))
        return

    artist = parts[0].strip()
    title = parts[1].strip()
    value = parts[2].strip()

    if value == "like":
        value_text = texts.get("rate_value_like")
    elif value == "dislike":
        value_text = texts.get("rate_value_dislike")
    elif value == "neutral":
        value_text = texts.get("rate_value_neutral")
    else:
        await query.edit_message_text(texts.get("error_generic"))
        return

    # Тут позже можно будет сохранить результат (в БД/файл/и т.д.)
    # user_id = update.effective_user.id

    message = texts.get(
        "rate_result",
        artist=artist,
        title=title,
        value=value_text,
    )

    # Убираем клавиатуру и показываем итог
    await query.edit_message_text(message)
