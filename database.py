import sqlite3

DB_NAME = "tickets.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL CHECK(length(title) <= 200),
        description TEXT CHECK(length(description) <= 2000),

        employee INTEGER,
        client INTEGER,

        date INTEGER NOT NULL,

        severity TEXT,
        status TEXT,
        category TEXT,

        room_id TEXT,

        latitude REAL,
        longitude REAL,

        email_team_leader TEXT CHECK(length(email_team_leader) <= 200)
    )
    """)

    conn.commit()
    conn.close()