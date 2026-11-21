# Rocky the Bull · Student Admissions Chatbot

Rocky answers questions about admissions, courses, enrollment, and student support for the University of South Florida's MS in Business Analytics and Information Systems program. Streamlit runs the chat interface, Ollama generates embeddings and answers, and Pinecone retrieves passages from the admissions knowledge base. SQLite stores chat transcripts, optional student registration details, and feedback.

## Set up and run

Use Python 3.12 or newer and [Ollama](https://ollama.com/download). Start the Ollama app or run `ollama serve`, then download the models in a separate terminal.

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Create a virtual environment and install the pinned dependencies in the repository directory. If you already have a `.env` file, keep it and compare its settings with `.env.example`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp -n .env.example .env
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` and copy the configuration file with `Copy-Item .env.example .env` when `.env` is absent.

Set `PINECONE_API_KEY` in `.env`. Set `PINECONE_INDEX_NAME` and `PINECONE_NAMESPACE` to match your knowledge base. The defaults are `student-admissions-ollama` and `__default__`. For a fresh knowledge base, ingest documents before asking questions.

```bash
python -m streamlit run chatbot.py
```

## Load admissions documents

The repository includes a concise knowledge file built from official USF admissions pages. To preview and upload it, run:

```bash
python ingest.py --dry-run
python ingest.py
```

The first command previews how many chunks are ready. The second embeds and uploads them. With no paths specified, the script reads existing `knowledge/`, `texts/`, and `pdfs/` directories. You can also pass your own PDF, Markdown, text file, or directory. For example, use `python ingest.py ~/Documents/usf-admissions` after replacing that example with a location that exists on your computer.

Add `--create-index` when the configured index does not exist. The script declares an `embedding` field sized to the configured Ollama model. The chatbot reads `chunk_text` and `title` from each match. See [Pinecone's document index documentation](https://sdk.pinecone.io/python/how-to/documents/schema-and-upsert.html).

Ingestion upserts stable chunk IDs based on file path, page, and position. Reruns can resume an interrupted upload. Ingestion leaves existing records outside the uploaded IDs in place, so use a fresh namespace for a full corpus replacement or an embedding model change. If the new model has a different vector dimension, use a new index. Keep the chat and ingestion settings in sync.

## Local records and email

The app initializes `student_chat_history.sqlite3` automatically. Set `CHAT_HISTORY_DB` in `.env` to use another path. The database check reports integrity and counts.

```bash
python check_database.py
python initialize_database.py --legacy-db
```

Run the second command only when migrating from the legacy `chat_history.db`. Add `--seed-csv` to import the historical CSV. Each option also accepts a custom source path. Imports preserve existing student profiles and skip previously imported transcripts. Imported timestamps record when the migration ran because the legacy records have no timestamps.

Registration is optional and intended for local demos with fictional student details. SQLite retains questions, answers, source excerpts, and feedback. Pinecone receives the search embedding, and Ollama receives the question and retrieved passages.

Email is disabled by default. To enable it, set `ENABLE_EMAIL_NOTIFICATIONS=true` and configure the SMTP variables in `.env.example`. Port 587 uses STARTTLS and port 465 uses implicit TLS. Rotate any SMTP credentials previously stored in Git.
