import pandas as pd
import sqlite3
import logging
from dotenv import load_dotenv
import os
from pathlib import Path


logging.basicConfig(level=logging.INFO)

load_dotenv()

data_dir = Path(os.getenv("DATA_DIR", "data"))
users_csv = data_dir / "user_listening_history.csv"
db_path = data_dir / "recs.db"

df = pd.read_csv(users_csv)

conn = sqlite3.connect(db_path)


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

logging.info("Migration started")

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

logging.info("Migration finished")
