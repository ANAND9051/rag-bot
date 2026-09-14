# What is this Project? (RAG Demystified)

This project is a **Retrieval-Augmented Generation (RAG)** application. It is one of the most important concepts to learn as an AI Automation Engineer.

---

## 💡 The Problem RAG Solves: "Hallucinations"
Large Language Models (LLMs) like GPT, Claude, or Gemini are trained on public internet data up to a certain point in time. 
If you ask an LLM:
*   *"What is my personal schedule for tomorrow?"*
*   *"What are the terms of this custom contract my company just signed?"*

The LLM cannot answer because it does not have access to your private files. If it tries to answer, it might make up convincing-sounding but completely false facts. This is called a **hallucination**.

---

## 🛠️ The Solution: Retrieval-Augmented Generation
Instead of retraining the LLM (which is very expensive and slow), RAG works by **giving the LLM the exact page/context it needs to answer the question right before it starts typing**.

Think of it like an **open-book exam**:
1. You ask a question.
2. The system searches your private documents ("the textbook") for the most relevant paragraphs.
3. It copies those paragraphs and pastes them into a prompt template.
4. It hands this prompt to the LLM (Gemini) and says: *"Answer the user's question, but use ONLY these paragraphs."*
5. The LLM reads the paragraphs and writes a 100% accurate, fact-checked answer.

---

## 🔄 The Two Phases of the Project

### Phase 1: Ingestion (`ingest.py`)
This is the "study phase" where documents are prepared.
1. **Extraction**: Reading the text from files (like PDF or TXT).
2. **Chunking**: Cutting long text into small, readable chunks (700 characters each).
3. **Embedding**: Converting text chunks into mathematical representation vectors.
4. **Storage**: Saving these vectors and chunks to our local database ([`vector_db.json`](../vector_db.json)).

### Phase 2: Q&A / Chat (`query.py`)
This is the "interactive phase" where the bot answers questions.
1. **Query Embedding**: Converts your question into a mathematical vector.
2. **Similarity Search**: Looks through [`vector_db.json`](../vector_db.json) and calculates the **Cosine Similarity** between your query vector and all document chunk vectors. It grabs the top 2 closest matching chunks.
3. **LLM Context Generation**: Passes the matching chunks to `gemini-2.5-flash` along with your question.
4. **Answer**: The LLM writes the final grounded response.
