import os

from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    users_csv: Path
    tracks_csv: Path
    popular_csv: Path
    db_path: Path


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "")
    data_dir = Path(os.getenv("DATA_DIR", "data"))

    bot_token = bot_token.strip()

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set. Put it in .env file")

    return Config(
        bot_token=bot_token,
        users_csv=data_dir / "user_listening_history.csv",
        tracks_csv=data_dir / "music_info.csv",
        popular_csv=data_dir / "popular_tracks.csv",
        db_path=data_dir / "recs.db",
    )


CONFIG = load_config()
