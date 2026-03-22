import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

_pool: SimpleConnectionPool = None


def init_db():
    global _pool
    _pool = SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        dsn=os.environ["DATABASE_URL"]
    )
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    balance INTEGER DEFAULT 1000
                )
            """)


@contextmanager
def _get_conn():
    """Borrow a connection from the pool and return it when done."""
    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)


def ensure_user(user_id: str):
    """Insert user with default balance if they don't exist."""
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING",
                (user_id,)
            )


def get_balance(user_id: str) -> int:
    ensure_user(user_id)
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT balance FROM users WHERE user_id = %s",
                (user_id,)
            )
            return cur.fetchone()[0]


def update_balance(user_id: str, delta: int) -> int:
    """Apply delta to balance and return the new balance."""
    ensure_user(user_id)
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET balance = balance + %s WHERE user_id = %s RETURNING balance",
                (delta, user_id)
            )
            return cur.fetchone()[0]
