import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.texts import Texts
from app.middlewares.texts import TextsMiddleware
from app.config import load_config

from app.handlers.start import router as start_router
from app.handlers.help import router as help_router
from app.handlers.setup_recommendations import router as setup_router
from app.handlers.get_rec import router as get_rec_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    config = load_config()

    bot = Bot(
        token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    texts = Texts("texts/ru.yml")

    # middleware: прокидываем texts в каждый хендлер параметром texts: Texts
    dp.update.middleware(TextsMiddleware(texts))
    dp.callback_query.middleware(TextsMiddleware(texts))

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(setup_router)
    dp.include_router(get_rec_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
