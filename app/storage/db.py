import aiosqlite
from app.config import CONFIG


async def init_db():
    async with aiosqlite.connect(CONFIG.db_path) as db:
        await db.executescript(
            """
        CREATE TABLE IF NOT EXISTS user_listening (
            user_id TEXT NOT NULL,
            track_id TEXT NOT NULL,
            playcount INTEGER NOT NULL,
            PRIMARY KEY (user_id, track_id)
        );
        """
        )
        await db.commit()
