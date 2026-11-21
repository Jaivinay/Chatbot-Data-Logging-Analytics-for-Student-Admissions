"""Project settings shared by the chatbot and maintenance scripts."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

DB_PATH = ROOT / Path(os.getenv("CHAT_HISTORY_DB") or "student_chat_history.sqlite3").expanduser()
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME") or "student-admissions-ollama"
NAMESPACE = os.getenv("PINECONE_NAMESPACE") or "__default__"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434"
CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL") or "llama3.2:3b"
EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL") or "nomic-embed-text"
EMBEDDING_FIELD = "embedding"
TEXT_FIELD = "chunk_text"
TITLE_FIELD = "title"
