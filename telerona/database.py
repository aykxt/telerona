import atexit
import logging

import psycopg2

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, database_url: str):
        self.conn = psycopg2.connect(database_url, sslmode="require")
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS users (chat_id INT PRIMARY KEY, first_name VARCHAR, last_name VARCHAR, username VARCHAR, phone INT, lang VARCHAR)"
        )
        self.conn.commit()
        c.close()
        logger.info("Database initialized.")
        atexit.register(self.close)

    def get_user_count(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM USERS")
        count = c.fetchone()[0]
        c.close()
        return count

    def init_user(self, user):
        c = self.conn.cursor()
        c.execute(
            f"INSERT INTO users (chat_id, first_name) VALUES ('{user.id}', '{user.first_name}')"
            f"ON CONFLICT (chat_id) DO UPDATE SET first_name = '{user.first_name}'"
        )

        if user.last_name:
            c.execute(
                f"UPDATE users SET last_name = '{user.last_name}' WHERE chat_id = '{user.id}'"
            )

        if user.phone:
            c.execute(
                f"UPDATE users SET phone = '{user.phone}' WHERE chat_id = '{user.id}'"
            )

        if user.username:
            c.execute(
                f"UPDATE users SET username = '{user.username}' WHERE chat_id = '{user.id}'"
            )

        if user.lang_code:
            c.execute(
                f"UPDATE users SET lang = '{user.lang_code}' WHERE chat_id = '{user.id}'"
            )

        self.conn.commit()
        c.close()

    def close(self):
        self.conn.close()
        logger.info("Connection closed.")
