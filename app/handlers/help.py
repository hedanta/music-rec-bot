from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.texts import Texts

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message, texts: Texts):
    """
    Показывает справку по боту
    """
    await message.answer(texts.get("help"))
