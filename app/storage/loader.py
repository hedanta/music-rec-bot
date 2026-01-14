import pandas as pd
import sqlite3
from app.config import load_config


def load_users_df() -> pd.DataFrame:
    """
    Загружает таблицу пользовательских взаимодействий из БД
    и преобразует к DataFrame

    :return: DataFrame с колонками user_id, track_id, playcount
    """
    config = load_config()
    conn = sqlite3.connect(config.db_path)
    df = pd.read_sql("SELECT user_id, track_id, playcount FROM user_listening", conn)
    conn.close()

    return df


def make_users_snapshot() -> pd.DataFrame:
    """
    Создаёт снэпшот текущей версии таблицы пользовательских
    взаимодействий

    :return: DataFrame с колонками user_id, track_id, playcount
    """
    return load_users_df().copy()
