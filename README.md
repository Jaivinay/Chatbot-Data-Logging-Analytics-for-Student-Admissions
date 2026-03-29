# LangChain Chatbot – BAIS Academic Assistant

## Overview

This project develops an AI-powered chatbot to support the MS Business Analytics and Information Systems (BAIS) program. It uses OpenAI GPT, LangChain, and Pinecone to provide accurate, context-aware responses to student queries.

The goal is to automate student support and improve response speed and consistency.

---

## Features

* LLM-based chatbot using OpenAI GPT
* Retrieval-Augmented Generation (RAG) with Pinecone
* Semantic search for relevant answers
* Streamlit interface for real-time interaction
* Handles queries on admissions, courses, and program details

---

## Architecture

1. User submits a query via Streamlit
2. Query is converted into embeddings
3. Pinecone retrieves relevant context
4. Context is combined with the query
5. GPT model generates the response

---

## Tech Stack

* Python
* LangChain
* OpenAI GPT
* Pinecone
* Streamlit

---

## Business Impact

* Reduces manual effort for academic staff
* Provides faster and consistent responses
* Enables 24/7 student support

---

## Note

Dataset is not publicly available due to privacy constraints.
