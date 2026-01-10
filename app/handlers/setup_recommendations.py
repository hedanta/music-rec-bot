from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.texts import Texts
from app.services.music import get_track_for_setup, save_track_rating

router = Router()

CB_PREFIX = "setup_rate:"


def _rating_kb(artist: str, title: str):
    kb = InlineKeyboardBuilder()
    base = f"{CB_PREFIX}{artist}|{title}|"

    kb.button(text="👍 Like", callback_data=base + "like")
    kb.button(text="😐 Neutral", callback_data=base + "neutral")
    kb.button(text="👎 Dislike", callback_data=base + "dislike")
    kb.adjust(3)
    return kb.as_markup()


@router.message(Command("setup_recommendations"))
async def setup_recommendations_handler(message: Message, texts: Texts) -> None:
    track = await get_track_for_setup(user_id=message.from_user.id)

    await message.answer(
        texts.get(
            "setup_track_message",
            artist=track.artist,
            title=track.title,
            url=track.spotify_url,
        ),
        reply_markup=_rating_kb(track.artist, track.title),
    )


@router.callback_query(F.data.startswith(CB_PREFIX))
async def setup_rate_callback(callback: CallbackQuery, texts: Texts) -> None:
    data = callback.data or ""
    payload = data[len(CB_PREFIX) :]
    parts = payload.split("|")
    if len(parts) != 3:
        await callback.answer(texts.get("error_generic"), show_alert=True)
        return

    artist, title, rating = (p.strip() for p in parts)
    if rating not in {"like", "neutral", "dislike"}:
        await callback.answer(texts.get("error_generic"), show_alert=True)
        return

    await save_track_rating(
        user_id=callback.from_user.id,
        artist=artist,
        title=title,
        rating=rating,
    )

    rating_text = texts.get(f"rate_value_{rating}")

    # 1) подтверждаем нажатие (убрать "часики")
    await callback.answer(texts.get("rate_saved_short", value=rating_text))

    # 2) обновляем текущее сообщение: убираем клавиатуру
    if callback.message:
        await callback.message.edit_reply_markup(reply_markup=None)

    # 3) присылаем следующий трек для сетапа (цикл)
    next_track = await get_track_for_setup(user_id=callback.from_user.id)
    if callback.message:
        await callback.message.answer(
            texts.get(
                "setup_track_message",
                artist=next_track.artist,
                title=next_track.title,
                url=next_track.spotify_url,
            ),
            reply_markup=_rating_kb(next_track.artist, next_track.title),
        )
