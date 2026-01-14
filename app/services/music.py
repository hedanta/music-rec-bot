from __future__ import annotations

from dataclasses import dataclass
from app.model.recommender import HybridRecommender


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


async def get_recommendation(user_id: int, recommender: HybridRecommender) -> Track:
    """
    Возвращает один рекомендованный трек на основе предпочтений.

    :param user_id: ID пользователя
    :param recommender: модель рекомендаций
    :return: рекомендованный трек
    """
    rec = recommender.recommend(str(user_id), n=1)

    return Track(
        track_id=rec[0]["track_id"],
        artist=rec[0]["artist"],
        title=rec[0]["name"],
        spotify_url=f"https://open.spotify.com/track/{rec[0]['spotify_id']}",
    )
