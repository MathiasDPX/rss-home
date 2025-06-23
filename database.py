from dotenv import load_dotenv
import psycopg2.extras
from os import getenv
import psycopg2

load_dotenv(".env")

class DatabaseConnection:
    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        conn_params = {
            "dbname": dbname or getenv("DB_NAME"),
            "user": user or getenv("DB_USERNAME"),
            "password": password or getenv("DB_PASSWORD"),
            "host": host or getenv("DB_HOST"),
            "port": port or getenv("DB_PORT")
        }

        self.conn = psycopg2.connect(**conn_params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

if __name__ == "__main__":
    dbconn = DatabaseConnection().conn