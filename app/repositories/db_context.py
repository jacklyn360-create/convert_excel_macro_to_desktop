from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config.settings import settings


class DatabaseContext:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path is not None else settings.db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_database()

    def initialize_database(self) -> None:
        with self.get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS responses (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    question TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    completion_time TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
