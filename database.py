# ============================================================
# database.py — SQLite data access layer
# ------------------------------------------------------------
# Wraps the existing plantdoc_users.db (users table already
# present) and adds a `predictions` table for history tracking.
#
# Demonstrates: relational schema design, parameterized queries
# (SQL-injection safe), connection handling, CRUD operations.
# ============================================================

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

DEFAULT_DB_PATH = 'plantdoc_users.db'


@contextmanager
def get_connection(db_path=None):
    """
    Context-managed SQLite connection with row factory for dict-like access.
    `db_path=None` resolves to the *current* module-level DEFAULT_DB_PATH at
    call time (not at import time), so app.py can override it at startup
    (e.g. for tests/CI) and every function here picks up the change.
    """
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path=None):
    """
    Idempotent schema initialization.
    `users` table already exists in the shipped DB (id, username,
    email, password) — CREATE IF NOT EXISTS keeps it untouched while
    guaranteeing the schema on a fresh database (e.g. in tests/CI).
    """
    with get_connection(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename TEXT NOT NULL,
                predicted_class TEXT NOT NULL,
                disease_name TEXT,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_predictions_user_id
            ON predictions(user_id)
        ''')


# ── User operations ─────────────────────────────────────────

def create_user(username, email, password, db_path=None):
    """Create a user with a securely hashed password. Returns new user id."""
    hashed = generate_password_hash(password)
    with get_connection(db_path) as conn:
        cur = conn.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed)
        )
        return cur.lastrowid


def get_user_by_username(username, db_path=None):
    with get_connection(db_path) as conn:
        row = conn.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        return dict(row) if row else None


def get_user_by_email(email, db_path=None):
    with get_connection(db_path) as conn:
        row = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        return dict(row) if row else None


def verify_user(username, password, db_path=None):
    """Return the user dict if credentials are valid, else None."""
    user = get_user_by_username(username, db_path)
    if user and check_password_hash(user['password'], password):
        return user
    return None


# ── Prediction history operations ───────────────────────────

def log_prediction(filename, predicted_class, disease_name, confidence,
                    user_id=None, db_path=None):
    with get_connection(db_path) as conn:
        cur = conn.execute(
            '''INSERT INTO predictions
               (user_id, filename, predicted_class, disease_name, confidence, created_at)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (user_id, filename, predicted_class, disease_name, confidence,
             datetime.now(timezone.utc).isoformat())
        )
        return cur.lastrowid


def get_history(user_id, limit=50, db_path=None):
    with get_connection(db_path) as conn:
        rows = conn.execute(
            '''SELECT id, filename, predicted_class, disease_name, confidence, created_at
               FROM predictions WHERE user_id = ?
               ORDER BY created_at DESC LIMIT ?''',
            (user_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]


def get_stats(db_path=None):
    """Aggregate stats — useful for an admin/analytics endpoint."""
    with get_connection(db_path) as conn:
        total_users = conn.execute('SELECT COUNT(*) AS c FROM users').fetchone()['c']
        total_predictions = conn.execute('SELECT COUNT(*) AS c FROM predictions').fetchone()['c']
        top_diseases = conn.execute(
            '''SELECT disease_name, COUNT(*) AS count FROM predictions
               WHERE disease_name IS NOT NULL
               GROUP BY disease_name ORDER BY count DESC LIMIT 5'''
        ).fetchall()
        return {
            'total_users': total_users,
            'total_predictions': total_predictions,
            'top_diseases': [dict(r) for r in top_diseases]
        }
