import pandas as pd
import sqlite3
import logging
from pathlib import Path

from app.config import CONFIG

df = pd.read_csv(CONFIG.users_csv)

conn = sqlite3.connect(CONFIG.db_path)

conn.executescript(
    """
CREATE TABLE IF NOT EXISTS user_listening (
    user_id TEXT NOT NULL,
    track_id TEXT NOT NULL,
    playcount INTEGER NOT NULL,
    PRIMARY KEY (user_id, track_id)
);
"""
)

df.to_sql(
    "user_listening",
    conn,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=10_000,
)

conn.commit()
conn.close()

logging.info("Migration done.")
