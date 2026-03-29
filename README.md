# LangChain Chatbot – AI-Powered BAIS Academic Assistant

## Overview

This project focuses on developing an LLM-based chatbot to support the MS Business Analytics and Information Systems (BAIS) program at the Muma College of Business. The chatbot leverages OpenAI GPT models, LangChain, and a Pinecone vector database to provide accurate, context-aware responses to student queries.

The objective is to automate and streamline student support, reduce manual workload for the Graduate Coordinator, and improve response speed and consistency.

---

## Key Features

* LLM-based chatbot using OpenAI GPT API
* Retrieval-Augmented Generation (RAG) with Pinecone vector database
* Semantic search for context-aware responses
* Prompt engineering for structured and accurate outputs
* Streamlit-based user interface for real-time interaction
* Integration of structured and unstructured data sources

---

## Supported Query Types

* Admissions information
* Courses and curriculum
* Program structure and requirements
* General student support queries

---

## Architecture

1. User submits a query through the Streamlit interface
2. Query is converted into embeddings
3. Pinecone vector database retrieves relevant context
4. Retrieved context is combined with the query (RAG pipeline)
5. OpenAI GPT model generates a context-aware response

---

## Tech Stack

* Python
* LangChain
* OpenAI GPT API
* Pinecone Vector Database
* Streamlit
* Semantic Search and Prompt Engineering

---

## Business Impact

* Reduced manual query handling for academic staff
* Improved response time and consistency
* Enabled 24/7 academic support
* Enhanced student experience and operational efficiency

---

## Use Case

The chatbot is designed to assist students by answering queries related to program details, course requirements, admission processes, and general FAQs for the BAIS program.

---

## Key Learnings

* Built end-to-end RAG pipelines using LangChain
* Integrated LLMs with vector databases
* Designed domain-specific prompt strategies
* Developed real-time AI applications with Streamlit

---

## Future Improvements

* Fine-tuned domain-specific language models
* Multi-turn conversational memory
* Integration with university systems via APIs
* Voice-enabled interaction

---

## Note

Due to data privacy and institutional constraints, the dataset used in this project is not publicly available.

