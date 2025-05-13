import os
import psycopg
from psycopg import Connection
from contextlib import contextmanager
from psycopg.rows import dict_row

# Use DATABASE_URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

@contextmanager
def get_connection() -> Connection:
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
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
