"""Check SQLite integrity and show record counts without printing student data."""

import argparse
import sqlite3
from pathlib import Path

from chat_history_db import database_connection
from config import DB_PATH


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DB_PATH, help="SQLite database to inspect")
    args = parser.parse_args()

    try:
        with database_connection(args.database, read_only=True) as connection:
            if connection.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
                parser.exit(1, "SQLite integrity check failed.\n")
            students = connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
            messages = connection.execute("SELECT COUNT(*) FROM chat_messages").fetchone()[0]
            feedback = connection.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    except sqlite3.Error as error:
        parser.exit(1, f"Could not check the database: {error}\n")

    print(f"SQLite integrity OK. Students: {students}, messages: {messages}, feedback: {feedback}.")


if __name__ == "__main__":
    main()
