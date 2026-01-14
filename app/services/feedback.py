import logging
from app.services.retrain_scheduler import on_feedback_event
from app.storage.storage import save_track_rating


async def handle_user_feedback(
    user_id: int,
    track_id: str,
    rating: str,
    recommender,
):
    """
    Обрабатывает полученную оценку от пользователя.
    Сохраняет запись в БД и обращается к ретрейнеру
    """
    await save_track_rating(user_id, track_id, rating)
    await on_feedback_event(recommender)
