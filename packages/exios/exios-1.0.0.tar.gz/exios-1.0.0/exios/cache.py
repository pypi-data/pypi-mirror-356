import sqlite3
from pathlib import Path

class exiosCache:
    def __init__(self, db_path="Cache/exios.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS cache (url TEXT PRIMARY KEY, response TEXT)")
        self.conn.commit()

    def get(self, url):
        row = self.conn.execute("SELECT response FROM cache WHERE url=?", (url,)).fetchone()
        return row[0] if row else None

    def set(self, url, response):
        self.conn.execute("REPLACE INTO cache (url, response) VALUES (?, ?)", (url, response))
        self.conn.commit()
