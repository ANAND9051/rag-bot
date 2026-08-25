import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from vector_db import SimpleVectorDB

# Load variables from .env file
load_dotenv()

# Verify that the Gemini API Key is set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
    print("[ERROR] Please set your GEMINI_API_KEY in the .env file.")
    sys.exit(1)

# Configure the Google Gemini SDK
genai.configure(api_key=api_key)

# Connect to our custom vector database
db = SimpleVectorDB()

# Check if the database has any documents
if not db.data:
    print("[ERROR] Vector database is empty. Please run 'python ingest.py' first to index your documents.")
    sys.exit(1)

def embed_query(query_text):
    """
    Generates semantic vector embeddings for the query using Gemini's embedding model.
    Note we use 'retrieval_query' task type here for optimal query embeddings.
    """
    try:
        response = genai.embed_content(
            model="models/gemini-embedding-001",
            content=query_text,
            task_type="retrieval_query"
        )
        return response['embedding']
    except Exception as e:
        print(f"[ERROR] Failed to embed query: {e}")
        return None

def ask_question(question):
    """
    Searches the vector database for relevant contexts, prompts the LLM, and prints the result.
    """
    print("\n--- Step 1: Embedding Query ---")
    query_vector = embed_query(question)
    if not query_vector:
        return
        
    print("--- Step 2: Retrieving Context from Custom Vector DB ---")
    # Query our custom database for the top 2 matching chunks
    results = db.query(query_vector, n_results=2)
    
    if not results:
        print("[WARN] No matching contexts found. Answering with general knowledge.")
        context = "No context available."
    else:
        print(f"Retrieved {len(results)} relevant segments:")
        retrieved_texts = []
        for similarity, item in results:
            snippet = item["text"][:120].replace('\n', ' ') + "..."
            source = item["metadata"].get("source", "unknown")
            print(f"  - [Similarity: {similarity:.4f} | Source: {source}]: {snippet}")
            retrieved_texts.append(item["text"])
        context = "\n---\n".join(retrieved_texts)

    print("\n--- Step 3: Generating Answer with Gemini LLM ---")
    # Build a prompt that forces the model to use the context
    prompt = f"""You are a precise Q&A assistant. Use ONLY the facts provided in the Context section below to answer the Question.
If the answer cannot be found in the provided context, state that you do not have enough information to answer. Do not use external facts.

Context:
{context}

Question:
{question}

Answer:"""

    try:
        # Using the fast, efficient gemini-2.5-flash model
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        print("\n--- Answer ---")
        print(response.text)
        print("-" * 30)
    except Exception as e:
        print(f"[ERROR] Failed to generate answer from LLM: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("       RAG Search & Q&A Terminal CLI (Gemini + Custom Vector DB)")
    print("       Type 'exit' or 'quit' to close the program.")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nAsk a question: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            ask_question(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
