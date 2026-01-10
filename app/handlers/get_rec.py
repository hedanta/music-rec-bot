from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.texts import Texts
from app.services.music import get_recommendation

router = Router()


@router.message(Command("get_rec"))
async def get_rec_handler(message: Message, texts: Texts) -> None:
    track = await get_recommendation(user_id=message.from_user.id)

    await message.answer(
        texts.get(
            "rec_message",
            artist=track.artist,
            title=track.title,
            url=track.spotify_url,
        )
    )
