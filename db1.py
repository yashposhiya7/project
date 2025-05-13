import psycopg
from psycopg import Connection
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "project",
    "user": "yash"
}

@contextmanager
def get_connection() -> Connection:
    conn = psycopg.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: tuple = None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            if cur.description:  # SELECT or RETURNING
                return cur.fetchall()
            conn.commit()
