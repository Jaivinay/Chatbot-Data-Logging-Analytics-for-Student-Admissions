"""Initialize SQLite and optionally import records from the legacy chatbot."""

import argparse
import csv
import hashlib
import sqlite3
from pathlib import Path

from chat_history_db import database_connection, initialize_database, timestamp
from config import DB_PATH, ROOT
from langchain_helpers import legacy_chat_messages


def seed_records(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        columns = ("email", "u_number", "name", "conversation")
        if not set(columns).issubset(reader.fieldnames or []):
            raise ValueError("Seed CSV requires email, u_number, name and conversation columns")
        return [tuple(row[column] for column in columns) for row in reader]


def import_records(connection, records):
    students = messages = 0
    imported_at = timestamp()
    for row_number, (email, u_number, name, conversation) in enumerate(records, start=1):
        email = (email or "").strip().lower()
        if not email:
            raise ValueError(f"Legacy record {row_number} has no email")
        try:
            transcript = legacy_chat_messages(conversation)
        except ValueError as error:
            raise ValueError(f"Legacy record {row_number} has an invalid transcript") from error

        students += connection.execute(
            "INSERT INTO students (email, full_name, u_number, created_at) "
            "VALUES (?, ?, ?, ?) ON CONFLICT(email) DO NOTHING",
            (email, (name or "").strip(), u_number, imported_at),
        ).rowcount
        if not transcript:
            continue

        session_id = "legacy-" + hashlib.sha256(email.encode()).hexdigest()
        if connection.execute(
            "SELECT 1 FROM chat_messages WHERE session_id = ? LIMIT 1", (session_id,)
        ).fetchone():
            continue

        connection.executemany(
            "INSERT INTO chat_messages (session_id, role, content, created_at) "
            "VALUES (?, ?, ?, ?)",
            [(session_id, role, content, imported_at) for role, content in transcript],
        )
        messages += len(transcript)
    return students, messages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DB_PATH, help="Target SQLite database")
    parser.add_argument(
        "--legacy-db", type=Path, nargs="?", const=ROOT / "chat_history.db",
        help="Import the legacy database, optionally from a specified path",
    )
    parser.add_argument(
        "--seed-csv", type=Path, nargs="?", const=ROOT / "users_deatils.csv",
        help="Import the legacy seed CSV, optionally from a specified path",
    )
    args = parser.parse_args()

    try:
        records = []
        if args.legacy_db:
            with database_connection(args.legacy_db, read_only=True) as source:
                records.extend(source.execute("SELECT email, u_number, name, conversation FROM users"))
        if args.seed_csv:
            records.extend(seed_records(args.seed_csv))

        initialize_database(args.database)
        with database_connection(args.database) as destination:
            students, messages = import_records(destination, records)
    except (OSError, sqlite3.Error, ValueError) as error:
        parser.exit(1, f"Database setup failed: {error}\n")

    print(f"Database ready. Imported {students} students and {messages} messages.")


if __name__ == "__main__":
    main()
