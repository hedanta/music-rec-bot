from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.texts import Texts

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, texts: Texts) -> None:
    await message.answer(texts.get("start"))
