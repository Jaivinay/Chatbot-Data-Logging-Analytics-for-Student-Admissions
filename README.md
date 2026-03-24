🤖 LangChain Chatbot – AI-Powered BAIS Academic Assistant
📌 Overview

This project focuses on developing an LLM-based chatbot to support the MS Business Analytics and Information Systems (BAIS) program at the Muma College of Business. The chatbot leverages OpenAI GPT models, LangChain, and a Pinecone vector database to provide accurate, context-aware responses to student queries.

The goal is to automate and streamline student support, reducing the workload on the Graduate Coordinator while improving response speed and consistency.

🚀 Key Features
💬 LLM-based Chatbot using OpenAI GPT API
🔍 Retrieval-Augmented Generation (RAG) with Pinecone vector database
📚 Answers queries related to:
Admissions
Courses & Curriculum
Program Details
General Student Support
⚡ Semantic Search for context-aware responses
🧠 Prompt Engineering for accurate and structured outputs
🌐 Streamlit UI for real-time interaction
🔗 Integration of structured and unstructured data sources
🏗️ Architecture
User inputs a query via Streamlit interface
Query is embedded and matched against Pinecone vector database
Relevant context is retrieved (RAG pipeline)
Context + query is passed to OpenAI GPT model
Model generates a context-aware response
🛠️ Tech Stack
Language: Python
LLM Framework: LangChain
LLM API: OpenAI GPT
Vector Database: Pinecone
Frontend: Streamlit
Other: Prompt Engineering, Semantic Search

🎯 Business Impact
Reduced manual query handling for the Graduate Coordinator
Improved response time and consistency for student queries
Enabled 24/7 academic support for BAIS students
Enhanced overall student experience and program efficiency
📂 Use Case

This chatbot is designed to handle a wide range of academic queries including:

Program structure and requirements
Course details and prerequisites
Admission guidelines
General FAQs related to BAIS
🔍 Key Learnings
Building end-to-end RAG pipelines
Integrating LLMs with external knowledge bases
Designing effective prompts for domain-specific tasks
Deploying AI applications with real-time user interaction
⚠️ Note

Due to data privacy and institutional constraints, the dataset used for this project is not publicly shared.

📌 Future Improvements
Fine-tuned domain-specific LLM
Multi-turn conversational memory
Integration with university systems (APIs)
Voice-based interaction
🤝 Contributions

Open to feedback and improvements. Feel free to fork and contribute!

⭐ If you found this project useful, consider giving it a star!
