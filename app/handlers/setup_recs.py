from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.texts import Texts
from app.services.music import get_track_for_setup
from app.services.feedback import handle_user_feedback
from app.services import get_recommender


router = Router()

CB_PREFIX = "setup_rate:"


def _rating_kb(track_id: str):
    kb = InlineKeyboardBuilder()
    base = f"{CB_PREFIX}{track_id}|"

    kb.button(text="👍", callback_data=base + "like")
    kb.button(text="😐", callback_data=base + "neutral")
    kb.button(text="👎", callback_data=base + "dislike")

    kb.button(
        text="Пропустить",
        callback_data=base + "skip",
    )

    kb.adjust(3, 1)

    return kb.as_markup()


@router.message(Command("setup_recs"))
async def setup_recommendations_handler(message: Message, texts: Texts):
    """
    Отправляет трек для оценки
    """
    recommender = await get_recommender()
    track = await get_track_for_setup(recommender=recommender)

    await message.answer(
        texts.get(
            "setup_track_message",
            artist=track.artist,
            title=track.title,
            url=track.spotify_url,
        ),
        reply_markup=_rating_kb(track.track_id),
    )


@router.callback_query(F.data.startswith(CB_PREFIX))
async def setup_rate_callback(callback: CallbackQuery, texts: Texts):
    """
    Обрабатывает нажатие на кнопку оценки или пропуска.
    Отправляет следующий трек для оценки.
    """
    data = callback.data or ""
    payload = data[len(CB_PREFIX) :]
    track_id, rating = payload.split("|", 1)
    recommender = await get_recommender()

    if rating != "skip":
        await handle_user_feedback(
            user_id=callback.from_user.id,
            track_id=track_id,
            rating=rating,
            recommender=recommender,
        )

        rating_text = texts.get(f"rate_value_{rating}")

        await callback.answer(texts.get("rate_saved_short", value=rating_text))
    else:
        await callback.answer(texts.get(f"rate_skip_short"))

    # присылаем следующий трек для сетапа (цикл)
    next_track = await get_track_for_setup(recommender=recommender)
    if callback.message:
        await callback.message.answer(
            texts.get(
                "setup_track_message",
                artist=next_track.artist,
                title=next_track.title,
                url=next_track.spotify_url,
            ),
            reply_markup=_rating_kb(next_track.track_id),
        )
