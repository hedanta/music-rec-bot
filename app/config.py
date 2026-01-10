import os

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    bot_lang: str


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "")
    bot_token = bot_token.strip()

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set. Put it in .env file")

    bot_lang = os.getenv("BOT_LANG", "ru")
    bot_lang = bot_lang.strip()

    if not bot_lang:
        bot_lang = "ru"

    return Config(
        bot_token=bot_token,
        bot_lang=bot_lang,
    )
