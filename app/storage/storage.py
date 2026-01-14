import aiosqlite
import logging
import pandas as pd

from app.config import CONFIG

RATING_TO_PLAYCOUNT = {
    "like": 20,
    "neutral": 5,
    "dislike": 1,
}

PLAYCOUNT_TO_RATING = {v: k for k, v in RATING_TO_PLAYCOUNT.items()}
RATING_ORDER = {"like": 0, "neutral": 1, "dislike": 2}


async def save_track_rating(
    user_id: int,
    track_id: str,
    rating: str,
):
    """
    Сохраняет оценку трека в БД, преобразуя рейтинг в количество прослушиваний
    для корректной работы модели

    :param user_id: ID пользователя
    :param track_id: ID трека
    :param rating: рейтинг (like/neutral/dislike)
    """
    delta = RATING_TO_PLAYCOUNT[rating]

    async with aiosqlite.connect(CONFIG.db_path) as db:
        await db.execute(
            """
            INSERT INTO user_listening (user_id, track_id, playcount)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, track_id)
            DO UPDATE SET playcount = excluded.playcount
            """,
            (str(user_id), track_id, delta),
        )
        await db.commit()

    logging.info(f"Rating saved | user: {user_id}, track: {track_id} - {rating}")


async def get_user_feedback(user_id: int, tracks: pd.DataFrame) -> list[dict[str, str]]:
    """
    Получает все оценки треков для конкретного пользователя

    :param user_id: ID пользователя
    :param tracks: DataFrame со всеми треками
    :return: список словарей вида {track_id, name, artist, rating}

    """
    async with aiosqlite.connect(CONFIG.db_path) as db:
        cursor = await db.execute(
            "SELECT track_id, playcount FROM user_listening WHERE user_id = ?",
            (str(user_id),),
        )
        rows = await cursor.fetchall()
        await cursor.close()

    feedbacks = []
    for track_id, playcount in rows:
        rating = PLAYCOUNT_TO_RATING.get(playcount, "neutral")

        track_row = tracks[tracks.track_id == track_id]
        name = track_row.iloc[0]["name"]
        artist = track_row.iloc[0]["artist"]

        feedbacks.append(
            {"track_id": track_id, "name": name, "artist": artist, "rating": rating}
        )

    feedbacks.sort(key=lambda f: RATING_ORDER.get(f["rating"]))

    return feedbacks
