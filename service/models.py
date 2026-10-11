
import os
import sqlite3


def get_connection():
    database = os.environ.get("DATABASE_PATH", "accounts.db")
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )


def row_to_dict(row):
    return dict(row) if row is not None else None
