from ..model.recommender import HybridRecommender
import logging
from app.storage.loader import make_users_snapshot

recommender: HybridRecommender | None = None


def init_recommender() -> HybridRecommender:
    """
    Инициализирует одну модель рекомендаций
    для всего бота
    """
    global recommender
    if recommender is None:
        logging.info("Initializing HybridRecommender")
        recommender = HybridRecommender()
        users_snapshot = make_users_snapshot()
        recommender.train(users_snapshot=users_snapshot)
        logging.info("HybridRecommender ready")
    return recommender


async def get_recommender() -> "HybridRecommender":
    return recommender
