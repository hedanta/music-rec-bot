import pandas as pd
import numpy as np
import logging

from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from app.config import CONFIG


class HybridRecommender:
    def __init__(self):
        self.model_cf = None
        self.user_item_matrix = None
        self.user2idx = None
        self.track2idx = None
        self.idx2track = None
        self.users = None
        self.X_scaled = None

        self.tracks = pd.read_csv(CONFIG.tracks_csv)
        self.popular_tracks = pd.read_csv(CONFIG.popular_csv)

    def load_snapshot(self, users_df: pd.DataFrame):
        """
        Записывает в таблицу пользовательских взаимодействий
        снэпшот из БД для корректного ретрейна

        :param users_df: DataFrame с колонками user_id, track_id, playcount
        """
        self.users = users_df

    def train(self, users_snapshot: pd.DataFrame):
        """
        Обучает модель

        :param users_snapshot: текущая таблица из БД в формате датафрейма
        """
        logging.info("Training started")

        self.load_snapshot(users_snapshot)

        self.users["rating"] = np.log1p(self.users["playcount"])

        user_codes = self.users["user_id"].astype("category")
        track_codes = self.users["track_id"].astype("category")

        self.user2idx = dict(
            zip(user_codes.cat.categories, range(len(user_codes.cat.categories)))
        )

        user_ids = user_codes.cat.codes
        track_ids = track_codes.cat.codes

        self.user_item_matrix = coo_matrix(
            (self.users["rating"], (user_ids, track_ids))
        ).tocsr()

        self.model_cf = AlternatingLeastSquares(
            factors=50, regularization=0.1, iterations=5
        )
        self.model_cf.fit(self.user_item_matrix)

        self._train_content()

        logging.info("Training finished")

    def _train_content(self):
        """
        Подготавливает признаки треков для контентной модели
        """
        audio_features = [
            "danceability",
            "energy",
            "valence",
            "tempo",
            "loudness",
            "acousticness",
            "instrumentalness",
            "liveness",
        ]
        X = self.tracks[audio_features].fillna(0)
        scaler = StandardScaler()
        self.X_scaled = scaler.fit_transform(X)

    def build_user_profile(self, user_id: str) -> np.ndarray:
        """
        Строит контентный профиль пользователя на основе прослушанных треков.

        :param user_id: ID пользователя
        :return: массив с усреднёнными фичами
        """
        listened = self.users[self.users.user_id == user_id]["track_id"]
        idx = self.tracks[self.tracks.track_id.isin(listened)].index

        return self.X_scaled[idx].mean(axis=0)

    def recommend_content(self, profile: np.ndarray) -> np.ndarray:
        """
        Вычисляет сходство профиля пользователя с треками
        с помощью косинусного сходства.

        :param profile: массив с профилем пользователя
        :return: массив схожести со всеми треками
        """
        scores = cosine_similarity(profile.reshape(1, -1), self.X_scaled)[0]

        return scores

    def recommend(
        self, user_id: str, alpha: float = 0.7, n: int = 1
    ) -> list[dict[str, str]]:
        """
        Составляет топ-N рекомендаций для пользователя, комбинируя CF и контентную модель.

        :param user_id: ID пользователя
        :param alpha: вес для коллаборативной фильтрации
        :param n: количество рекомендаций
        :return: список словарей с полями name, artist, track_id, spotify_id
        """
        # Получаем числовой индекс пользователя по его user_id
        user_index = self.user2idx[user_id]
        # Получаем строку взаимодействий для конкретного пользователя из матрицы пользователь-элемент.
        # user_item_matrix имеет формат (пользователи x элементы).
        user_interactions = self.user_item_matrix.getrow(user_index)

        # Получаем рекомендации от CF-модели
        cf_items, cf_scores = self.model_cf.recommend(
            user_index, user_interactions, N=50, filter_already_liked_items=True
        )

        # Строим профиль пользователя на основе его прослушанных треков и их характеристик
        profile = self.build_user_profile(user_id)

        # Получаем рекомендации на основе схожести треков
        content_scores = self.recommend_content(profile)

        # Объединяем оценки от CF и контентного подхода
        final_scores = {}

        for i, s in zip(cf_items, cf_scores):
            final_scores[i] = alpha * s

        top_content = np.argsort(content_scores)[-200:]

        for i, s in enumerate(top_content):
            final_scores[i] = final_scores.get(i, 0) + (1 - alpha) * s

        top_items = sorted(final_scores, key=final_scores.get, reverse=True)[:n]

        return self.tracks.iloc[top_items][
            ["name", "artist", "track_id", "spotify_id"]
        ].to_dict(orient="records")
