import sqlite3


def get_connection():
    conn = sqlite3.connect("users.db")

    conn.row_factory = sqlite3.Row

    return conn

def init_database():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()

    conn.close()


