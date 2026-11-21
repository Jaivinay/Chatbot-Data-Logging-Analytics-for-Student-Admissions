"""Load verified admissions documents into the chatbot's Pinecone index."""

import argparse
import hashlib
import os
from itertools import batched
from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, SchemaBuilder
from pinecone.errors import ConflictError, NotFoundError
from pypdf import PdfReader
from pypdf.errors import PyPdfError

from config import (
    EMBEDDING_FIELD,
    EMBEDDING_MODEL,
    INDEX_NAME,
    NAMESPACE,
    OLLAMA_BASE_URL,
    ROOT,
    TEXT_FIELD,
    TITLE_FIELD,
)

SUPPORTED_SUFFIXES = {".md", ".pdf", ".txt"}
BATCH_SIZE = 32


def document_paths(inputs):
    files = set()
    for path in inputs:
        if path.is_dir():
            files.update(
                item.resolve() for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in SUPPORTED_SUFFIXES
            )
        elif path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            files.add(path.resolve())
        else:
            raise ValueError(f"Expected a directory or a PDF, Markdown, or text file: {path}")
    return sorted(files)


def source_sections(path):
    if path.suffix.lower() == ".pdf":
        with path.open("rb") as source:
            for page_number, page in enumerate(PdfReader(source).pages, start=1):
                yield page_number, page.extract_text()
    else:
        yield 0, path.read_text(encoding="utf-8-sig")


def load_chunks(paths):
    splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    chunks = []
    for path in paths:
        source = Path(os.path.relpath(path, ROOT)).as_posix()
        count = len(chunks)
        for page, text in source_sections(path):
            title = f"{path.name} (page {page})" if page else path.name
            for position, chunk in enumerate(splitter.split_text(text)):
                chunk_id = hashlib.sha256(f"{source}\0{page}\0{position}".encode()).hexdigest()
                chunks.append({"_id": chunk_id, TITLE_FIELD: title, TEXT_FIELD: chunk})
        if len(chunks) == count:
            print(f"No extractable text in {path.name}; skipping.")
    return chunks


def open_index(client, dimension, create_index):
    try:
        index = client.indexes.describe(INDEX_NAME)
    except NotFoundError:
        if not create_index:
            raise ValueError(f"Index {INDEX_NAME!r} is missing. Rerun with --create-index to create it.")
        schema = SchemaBuilder().add_dense_vector_field(
            EMBEDDING_FIELD, dimension=dimension, metric="cosine"
        ).build()
        try:
            index = client.indexes.create(name=INDEX_NAME, schema=schema, timeout=120)
        except ConflictError:
            index = client.indexes.describe(INDEX_NAME)

    fields = index.schema.fields if index.schema else {}
    if getattr(fields.get(EMBEDDING_FIELD), "dimension", None) != dimension:
        raise ValueError(
            f"Index {INDEX_NAME!r} needs a document schema with a "
            f"{dimension}-dimension {EMBEDDING_FIELD!r} field. Select a compatible index."
        )
    if not index.status.ready or not index.host:
        raise ValueError(f"Index {INDEX_NAME!r} is still initializing. Retry when it is ready.")
    return client.index(host=index.host)


def upload_chunks(chunks, api_key, create_index):
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL, client_kwargs={"timeout": 120}
    )
    with Pinecone(api_key=api_key, timeout=30) as client:
        index = None
        uploaded = 0
        try:
            for batch in batched(chunks, BATCH_SIZE):
                vectors = embeddings.embed_documents([chunk[TEXT_FIELD] for chunk in batch])
                documents = [
                    {**chunk, EMBEDDING_FIELD: vector}
                    for chunk, vector in zip(batch, vectors, strict=True)
                ]
                if index is None:
                    index = open_index(client, len(vectors[0]), create_index)
                result = index.documents.upsert(namespace=NAMESPACE, documents=documents)
                if result.upserted_count != len(documents):
                    raise RuntimeError("Pinecone did not confirm the full batch. Rerun to retry.")
                uploaded += result.upserted_count
        finally:
            if index is not None:
                index.close()
    return uploaded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        type=Path,
        nargs="*",
        help="Documents or directories (default: knowledge/, texts/, and pdfs/)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Read and split local documents without uploading")
    parser.add_argument("--create-index", action="store_true", help="Create the configured index if it does not exist")
    args = parser.parse_args()

    try:
        default_directories = (ROOT / "knowledge", ROOT / "texts", ROOT / "pdfs")
        inputs = args.paths or [path for path in default_directories if path.is_dir()]
        paths = document_paths(inputs)
        chunks = load_chunks(paths)
        if not chunks:
            parser.error("No text found. Provide a PDF with selectable text, Markdown, or UTF-8 text.")

        print(f"Prepared {len(chunks)} chunks from {len(paths)} files.")
        if args.dry_run:
            return

        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            parser.error("Set PINECONE_API_KEY before uploading documents.")
        uploaded = upload_chunks(chunks, api_key, args.create_index)
    except (OSError, ValueError, PyPdfError) as error:
        parser.exit(1, f"Ingestion failed: {error}\n")
    except Exception as error:
        parser.exit(1, f"Ingestion failed ({type(error).__name__}). Check Ollama and Pinecone connectivity.\n")

    print(f"Uploaded {uploaded} chunks to {INDEX_NAME!r}, namespace {NAMESPACE!r}.")


if __name__ == "__main__":
    main()
