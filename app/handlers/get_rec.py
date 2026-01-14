from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.texts import Texts
from app.services import get_recommender
from app.services.music import get_recommendation
from app.services.feedback import handle_user_feedback
from app.storage.storage import get_user_feedback

router = Router()

CB_PREFIX_REC = "rec_rate:"


def _rec_rating_kb(track_id: str):
    kb = InlineKeyboardBuilder()
    base = f"{CB_PREFIX_REC}{track_id}|"

    kb.button(text="👍", callback_data=base + "like")
    kb.button(text="😐", callback_data=base + "neutral")
    kb.button(text="👎", callback_data=base + "dislike")

    kb.adjust(3)

    return kb.as_markup()


@router.message(Command("get_rec"))
async def get_rec_handler(message: Message, texts: Texts) -> None:
    """
    Отправляет рекомендованный трек с клавиатурой для оценки
    """
    recommender = await get_recommender()
    feedbacks = await get_user_feedback(message.from_user.id, recommender.tracks)

    if len(feedbacks) < 6:
        return await message.answer(texts.get("need_rates"))

    track = await get_recommendation(
        user_id=message.from_user.id, recommender=recommender, n=5
    )

    if track is None:
        return await message.answer(texts.get("no_more_recs"))

    await message.answer(
        texts.get(
            "rec_message",
            artist=track.artist,
            title=track.title,
            url=track.spotify_url,
        ),
        reply_markup=_rec_rating_kb(track.track_id),
    )


@router.callback_query(F.data.startswith(CB_PREFIX_REC))
async def rec_rate_callback(callback: CallbackQuery, texts: Texts):
    """
    Обрабатывает нажатия на кнопки оценки
    """
    data = callback.data or ""
    payload = data[len(CB_PREFIX_REC) :]
    track_id, rating = payload.split("|", 1)
    recommender = await get_recommender()

    if rating not in {"like", "neutral", "dislike"}:
        return await callback.answer(texts.get("error_generic"), show_alert=True)

    await handle_user_feedback(
        user_id=callback.from_user.id,
        track_id=track_id,
        rating=rating,
        recommender=recommender,
    )
    rating_text = texts.get(f"rate_value_{rating}")
    await callback.answer(texts.get("rate_saved_short", value=rating_text))

    next_track = await get_recommendation(
        user_id=callback.from_user.id, recommender=recommender
    )

    if next_track is None:
        return await callback.message.edit_text(texts.get("no_more_recs"))

    await callback.message.answer(
        texts.get(
            "rec_message",
            artist=next_track.artist,
            title=next_track.title,
            url=next_track.spotify_url,
        ),
        reply_markup=_rec_rating_kb(next_track.track_id),
    )
