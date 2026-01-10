import logging

from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler

from app.config import load_config
from app.texts import load_texts

from app.handlers.start_help import start_handler, help_handler
from app.handlers.whoami import whoami_handler
from app.handlers.rate import rate_handler, rate_callback_handler
from app.handlers.recommendations import (
    getrecommendation_handler,
    myrecommendations_handler,
)


def build_application() -> Application:
    config = load_config()
    texts = load_texts(config.bot_lang)

    application = Application.builder().token(config.bot_token).build()

    application.bot_data["texts"] = texts

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("whoami", whoami_handler))

    application.add_handler(CommandHandler("rate", rate_handler))
    application.add_handler(CommandHandler("rate", rate_handler))
    application.add_handler(
        CallbackQueryHandler(rate_callback_handler, pattern="^rate:")
    )

    application.add_handler(
        CommandHandler("getrecommendation", getrecommendation_handler)
    )
    application.add_handler(
        CommandHandler("myrecommendations", myrecommendations_handler)
    )

    return application


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )

    application = build_application()
    application.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
