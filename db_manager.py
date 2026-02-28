import sqlite3
from datetime import datetime

DB_PATH = "database/neurofocus.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            focus INTEGER,
            xp INTEGER,
            level INTEGER,
            seconds INTEGER
        )
    """)
    conn.commit()
    conn.close()

def log_session(focus, xp, level, seconds):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sessions (timestamp, focus, xp, level, seconds) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), focus, xp, level, seconds),
    )
    conn.commit()
    conn.close()
def export_csv():
    import csv
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions")
    rows = cur.fetchall()
    conn.close()

    with open("database/export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id","timestamp","focus","xp","level","seconds"])
        writer.writerows(rows)

def get_today_stats():
    """Return aggregated stats for sessions that occurred today.

    The returned tuple is (total_focus, total_xp, session_count).
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # SQLite datetime comparison using date strings
    cur.execute(
        """
        SELECT
            COALESCE(SUM(focus),0),
            COALESCE(SUM(xp),0),
            COUNT(*)
        FROM sessions
        WHERE date(timestamp) = date('now')
        """
    )
    row = cur.fetchone()
    conn.close()
    return row if row is not None else (0, 0, 0)
def get_today_stats():
    import sqlite3
    from datetime import date
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("""
        SELECT AVG(focus), MAX(xp), MAX(level)
        FROM sessions
        WHERE timestamp LIKE ?
    """, (today + "%",))
    row = cur.fetchone()
    conn.close()
    return row or (0, 0, 1)    