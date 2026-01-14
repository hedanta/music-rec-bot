from typing import Dict
from collections import deque
from dataclasses import dataclass
from app.model.recommender import HybridRecommender


USER_RECS: Dict[int, deque] = {}


@dataclass(frozen=True)
class Track:
    track_id: str
    artist: str
    title: str
    spotify_url: str


async def get_track_for_setup(recommender: HybridRecommender) -> Track:
    """
    Возвращает случайный трек для оценки

    :return: трек для оценки
    """
    row = recommender.popular_tracks.sample(
        1, weights=recommender.popular_tracks["playcount"]
    ).iloc[0]

    return Track(
        track_id=row["track_id"],
        artist=row["artist"],
        title=row["name"],
        spotify_url=f"https://open.spotify.com/track/{row['spotify_id']}",
    )


"""
async def get_recommendation(user_id: int, recommender: HybridRecommender, n: int) -> Track:
    
    Возвращает n рекомендованных треков на основе предпочтений.

    :param user_id: ID пользователя
    :param recommender: модель рекомендаций
    :param n: количество возвращаемых рекомендаций
    :return: рекомендованный трек
    
    recs = recommender.recommend(str(user_id), n=n)

    return [
        Track(
            track_id=r["track_id"],
            artist=r["artist"],
            title=r["name"],
            spotify_url=f"https://open.spotify.com/track/{r['spotify_id']}",
        )
        for r in recs
    ]
"""


async def get_recommendation(
    user_id: int, recommender, n: int = 5
) -> dict[str, str] | None:
    """
    Возвращает следующий трек для пользователя.
    При первом вызове формирует очередь из n рекомендаций.
    Если очередь пуста — возвращает None.
    """
    if user_id not in USER_RECS:
        recs = recommender.recommend(str(user_id), n=n)

        USER_RECS[user_id] = deque(
            Track(
                track_id=r["track_id"],
                artist=r["artist"],
                title=r["name"],
                spotify_url=f"https://open.spotify.com/track/{r['spotify_id']}",
            )
            for r in recs
        )

    if not USER_RECS[user_id]:
        return None

    return USER_RECS[user_id].popleft()
