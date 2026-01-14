import asyncio
import logging
from app.storage.loader import make_users_snapshot

BATCH_SIZE = 6

_events_since_retrain = 0
_retrain_lock = asyncio.Lock()


async def on_feedback_event(recommender):
    """
    Вызывается после получения оценки.
    Если пришло оценок согласно размеру батча,
    то блокирует возможность ретрейна и запускает функцию ретрейна.
    """
    global _events_since_retrain

    _events_since_retrain += 1

    if _events_since_retrain < BATCH_SIZE:
        return

    async with _retrain_lock:
        _events_since_retrain = 0

        asyncio.create_task(_run_retrain(recommender))


async def _run_retrain(recommender):
    """
    В фоне вызывает трейн модели на снэпшоте из БД
    """
    logging.info("Retrain called")

    loop = asyncio.get_running_loop()

    users_snapshot = await loop.run_in_executor(None, make_users_snapshot)

    await loop.run_in_executor(None, recommender.train, users_snapshot)
