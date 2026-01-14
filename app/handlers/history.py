from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.storage.storage import get_user_feedback
from app.services import get_recommender
from app.texts import Texts

router = Router()


@router.message(Command("history"))
async def history_handler(message: Message, texts: Texts):
    """
    Показывает историю оценок в формате "трек-исполнитель-оценка"
    """
    user_id = message.from_user.id
    recommender = await get_recommender()
    feedbacks = await get_user_feedback(user_id, recommender.tracks)

    if not feedbacks:
        return await message.answer(texts.get("history_empty"))

    rating_emoji_dict = texts.get_dict("rate_emoji")

    lines = []
    for f in feedbacks:
        rating_emoji = rating_emoji_dict.get(f["rating"])
        line = texts.get(
            "history_line",
            name=f["name"],
            artist=f["artist"],
            rating_emoji=rating_emoji,
        )
        lines.append(line)

    history_text = "\n".join(lines)
    await message.answer(history_text)
