"""SQLite storage for student profiles, chat transcripts, and feedback."""

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from config import DB_PATH


@contextmanager
def database_connection(path=None, *, read_only=False):
    path = Path(path if path is not None else DB_PATH).resolve()
    target = f"{path.as_uri()}?mode=ro" if read_only else path
    connection = sqlite3.connect(target, uri=read_only)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def timestamp():
    return datetime.now(UTC).isoformat()


def initialize_database(path=None):
    with database_connection(path) as connection:
        connection.executescript("""
            BEGIN;
            CREATE TABLE IF NOT EXISTS students (
                email TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                u_number TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                student_email TEXT,
                rating TEXT NOT NULL,
                comments TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                sources_json TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS chat_messages_session_id
                ON chat_messages (session_id, id);
            COMMIT;
        """)


def save_message(session_id, role, content, sources=None):
    with database_connection() as connection:
        connection.execute(
            "INSERT INTO chat_messages (session_id, role, content, sources_json, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (session_id, role, content, json.dumps(sources or []), timestamp()),
        )


def load_messages(session_id):
    with database_connection(read_only=True) as connection:
        rows = connection.execute(
            "SELECT role, content, sources_json FROM chat_messages "
            "WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
    return [
        {"role": role, "content": content, "sources": json.loads(sources_json)}
        for role, content, sources_json in rows
    ]


def register_student(email, full_name, u_number=""):
    with database_connection() as connection:
        connection.execute(
            "INSERT INTO students (email, full_name, u_number, created_at) "
            "VALUES (?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET "
            "full_name = excluded.full_name, "
            "u_number = COALESCE(NULLIF(excluded.u_number, ''), students.u_number)",
            (email.strip().lower(), full_name.strip(), u_number.strip(), timestamp()),
        )


def save_feedback(session_id, email, rating, comments):
    with database_connection() as connection:
        connection.execute(
            "INSERT INTO feedback (session_id, student_email, rating, comments, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (session_id, email or None, rating, comments, timestamp()),
        )
