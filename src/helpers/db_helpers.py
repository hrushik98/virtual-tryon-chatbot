import sqlite3
from typing import Optional

DATABASE_URL = "user_data.db"


def init_db() -> None:
    """Initializes the SQLite database if not already existing."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_images (
        user_id TEXT PRIMARY KEY,
        person_url TEXT,
        garment_url TEXT
    )
    ''')
    conn.commit()
    conn.close()


def store_in_db(user_id: str, key: str, value: str) -> None:
    """Stores or updates the URL in the database for a given user."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM user_images WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    if row:
        cursor.execute(f'UPDATE user_images SET {key} = ? WHERE user_id = ?', (value, user_id))
    else:
        if key == 'person_url':
            cursor.execute(
                'INSERT INTO user_images (user_id, person_url, garment_url) VALUES (?, ?, ?)', 
                (user_id, value, None)
            )
        elif key == 'garment_url':
            cursor.execute(
                'INSERT INTO user_images (user_id, person_url, garment_url) VALUES (?, ?, ?)', 
                (user_id, None, value)
            )

    conn.commit()
    conn.close()


def retrieve_from_db(user_id: str, key: str) -> Optional[str]:
    """Retrieves the URL from the database for a given user and key."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(f'SELECT {key} FROM user_images WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def reset_user_session(user_id: str) -> None:
    """Resets the user session by deleting the user entry from the database."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM user_images WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
