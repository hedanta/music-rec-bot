from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    artist: str
    title: str
    spotify_url: str


async def get_track_for_setup(user_id: int) -> Track:
    """
    Заглушка: трек для 'пролайкать треки для рекомендаций'
    """
    return Track(
        artist="Daft Punk",
        title="Harder, Better, Faster, Stronger",
        spotify_url="https://open.spotify.com/track/placeholder_setup",
    )


async def get_recommendation(user_id: int) -> Track:
    """
    Заглушка: рекомендация на основе предпочтений.
    """
    return Track(
        artist="Radiohead",
        title="Creep",
        spotify_url="https://open.spotify.com/track/placeholder_rec",
    )


async def save_track_rating(
    user_id: int,
    artist: str,
    title: str,
    rating: str,  # "like" | "neutral" | "dislike"
) -> None:
    """
    Заглушка сохранения оценки.
    """
    # TODO: подключить БД/файл и реально сохранять
    return None
