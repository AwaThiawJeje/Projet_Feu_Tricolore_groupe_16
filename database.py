import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="database_thies.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS logs")
            self.cursor.execute("""
                CREATE TABLE logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    type TEXT,
                    action TEXT,
                    scenario TEXT
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Erreur DB Setup: {e}")

    def log(self, log_type, action, scenario):
        timestamp = datetime.now().strftime("%H:%M:%S")
        try:
            self.cursor.execute(
                "INSERT INTO logs (timestamp, type, action, scenario) VALUES (?, ?, ?, ?)",
                (timestamp, log_type, action, scenario)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur Log: {e}")

    def clear_logs(self):
        self.cursor.execute("DELETE FROM logs")
        self.conn.commit()

    def get_logs(self, limit=20):
        try:
            self.cursor.execute("SELECT timestamp, type, action FROM logs ORDER BY id DESC LIMIT ?", (limit,))
            return self.cursor.fetchall()
        except:
            return []
