import sqlite3
from contextlib import contextmanager
from typing import Generator
from app.core.config import settings

def init_db() -> None:
    # Create the database file if it doesn't exist
    with sqlite3.connect(settings.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status NOT NULL DEFAULT 'pending',
                priority TEXT NOT NULL DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()            

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection,None,None]:
    conn = sqlite3.connect(settings.db_path)
    try:
        yield conn
        conn.commit()
    except Exception :
        conn.rollback()
        raise
    finally:
        conn.close()