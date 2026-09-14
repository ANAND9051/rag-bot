# Technologies & Concepts Used in this Project

Here are the details of the tools and engineering concepts utilized in this RAG codebase.

---

## 1. Vector Embeddings (`gemini-embedding-001`)
An embedding model converts a string of text into a vector (a list of 768 decimal numbers).
*   **Why is this useful?** Words that mean similar things are closer to each other in vector space. For example, if you query *"How do I solve bugs?"*, the model can match it to a document chunk that says *"Debugging error reports"* even though the word "bugs" is not in that chunk! This is called **Semantic Search**.
*   **Task Types**:
    *   `retrieval_document`: Used when embedding the document chunks to optimize them for database storage.
    *   `retrieval_query`: Used when embedding the user's question to optimize it for searching.

---

## 2. Cosine Similarity Math
How do we find which vectors in our database match our query vector? We measure the angle between them using **Cosine Similarity**.
*   If two vectors point in the exact same direction (very similar meaning), the cosine similarity score is `1.0`.
*   If they are perpendicular (unrelated), the score is `0.0`.
*   Our custom [`vector_db.py`](../vector_db.py) calculates this using a simple loop over the vector arrays.

---

## 3. Large Language Model (`gemini-2.5-flash`)
We use Gemini 2.5 Flash for the final answer generation.
*   **Why Flash?** It is extremely fast, highly cost-effective, and supports a massive context window (up to 1 million tokens).
*   **Prompting constraints**: In [`query.py`](../query.py), we construct a prompt instructing the LLM: *"Use ONLY the facts provided in the Context section. If the answer cannot be found, state that you do not have enough information."* This forces the LLM to remain grounded.

---

## 4. Local File-Based Storage (`vector_db.json`)
Instead of installing an enterprise database engine (like Pinecone or PostgreSQL pgvector), we build a local file-based database.
*   **How it works**: When chunks are processed, the Python lists and floats are dumped into a standard JSON file.
*   **Benefit**: You can open [`vector_db.json`](../vector_db.json) in any text editor and see exactly what vectors look like. It is 100% transparent and requires zero setup/installation.

---

## 5. Chunking & Overlap
When reading [`sample_doc.txt`](../sample_doc.txt), we split it into segments of **700 characters** with an **overlap of 150 characters**.
*   **Why chunk size is 700**: If chunks are too small, they lose context. If they are too big, they contain too much noise and waste API tokens.
*   **Why overlap is 150**: Overlapping ensures that a sentence split right in the middle during chunking isn't lost. The meaning is carried over to the next chunk.
