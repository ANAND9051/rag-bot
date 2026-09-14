# Document Q&A Bot (Production RAG with Pinecone & Google Gemini)

An enterprise-grade Retrieval-Augmented Generation (RAG) system built with **Pinecone** (the official, dedicated cloud vector database) and **Google Gemini** (`gemini-2.5-flash` + `gemini-embedding-001`).

---

## 🏗️ Architecture Overview

```
                         [ User Documents (.txt / .pdf) ]
                                        │
                                        ▼
                  [ Recursive Boundary-Aware Chunking ]
                        (Paragraphs / Sentences / Words)
                                        │
                                        ▼
                   [ Dense Vector Embeddings (Gemini) ]
                        (task_type: RETRIEVAL_DOCUMENT)
                                        │
                                        ▼
               [ Pinecone Cloud Serverless Index ('rag-bot') ]
                   (Cosine Similarity | AWS us-east-1)
                                        │
                         [ Real-Time Q&A Terminal CLI ]
```

### Query Flow:
1. **Multi-Document Ingestion**: Supports single files, multiple PDFs, and directories simultaneously (`python ingest.py doc1.pdf doc2.pdf`).
2. **Semantic Query Embedding**: Converts user queries into 768-dimensional normalized vectors with `taskType="RETRIEVAL_QUERY"`.
3. **Pinecone Vector Search**: Queries the hosted Pinecone cloud index with sub-millisecond similarity matching.
4. **Context Construction & Citations**: Extracts matching text and metadata (file source, page numbers, chunk IDs).
5. **Grounded Generation**: Prompts `gemini-2.5-flash` with strict hallucination-prevention guardrails to answer solely based on verified document context.

---

## ⚡ Production Features

| Feature | Description |
|---|---|
| **Official Vector DB** | Hosted, serverless cloud index on **Pinecone** with real-time web dashboard |
| **Multi-Doc Ingestion** | Ingest multiple PDFs/text files in a single run; searches across all of them |
| **Multimodal Vision OCR** | Automatically transcribes scanned, image-only, or handwritten PDFs via Gemini Flash |
| **Boundary-Aware Chunking** | Splits text on paragraphs, sentences, and words—never slicing words in half |
| **Source Citations** | Explicitly cites source files (`[Source #1 \| File: java_course.pdf]`) |
| **Hallucination Guardrail** | Fails gracefully when documents do not contain the answer |

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
cd C:/Users/anand/rag_bot
python -m pip install -r requirements.txt
```

### 2. Configure API Keys
Add your keys to `.env` in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

---

## 🏃 Usage

### Step 1: Ingest Documents (Single or Multiple)
```bash
# Ingest single or multiple files into Pinecone
python ingest.py docs/java_course.pdf sample_doc.txt --clear

# Ingest all documents in a folder
python ingest.py docs/
```

### Step 2: Start Interactive Q&A
```bash
python query.py
```

Try asking:
* *"What are the flavors of Java according to the course?"*
* *"What are the main benefits of RAG?"*
* *"What is the weather in Tokyo?"* *(Tests the hallucination guardrail)*

---

## 📊 Inspect Vectors in Pinecone Web Console
You can view your live vectors, metadata payloads, and index metrics directly in the Pinecone dashboard at **[app.pinecone.io](https://app.pinecone.io)** under the index **`rag-bot`**.

---

## 📸 Demo Screenshots

### Multi-Document Q&A with Pinecone Cloud & Inline Citations:
![Pinecone Query Demo 1](assets/Screenshot%202026-09-14%20141618.png)

### Real-Time Retrieval & Hallucination Guardrails:
![Pinecone Query Demo 2](assets/Screenshot%202026-09-14%20141715.png)
