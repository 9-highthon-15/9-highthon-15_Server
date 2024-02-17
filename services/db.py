import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.dbInit()

    def __del__(self):
        self.conn.close()

    def dbInit(self):
        self.cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='diary'
            """
        )
        if not self.cursor.fetchone():
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user (
                    uuid TEXT PRIMARY KEY NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    nickname TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    region TEXT NOT NULL,
                    image TEXT
                )
                """
            )

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS post (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uuid TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    FOREIGN KEY(uuid) REFERENCES user(uuid)
                )
                """
            )

            self.conn.commit()

    def query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid
