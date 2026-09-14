import os
import sys
import time
from gemini_client import GeminiClient
from vector_db import PineconeVectorDB

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def format_context(results):
    """
    Formats retrieved search results into a clean, numbered context block with citations.
    """
    context_blocks = []
    for rank, (score, doc) in enumerate(results, 1):
        meta = doc.get("metadata", {})
        source = os.path.basename(meta.get("source", "unknown"))
        page = f" (Page {meta['page']})" if "page" in meta else ""
        chunk_id = meta.get("chunk_index", doc.get("id"))

        header = f"[Source #{rank} | File: {source}{page} | Chunk ID: {chunk_id} | Similarity: {score:.4f}]"
        context_blocks.append(f"{header}\n{doc['text']}")
    return "\n\n".join(context_blocks)

def ask_question(question: str, client: GeminiClient, db: PineconeVectorDB, top_k: int = 3):
    """
    RAG Query Flow:
    1. Embed query vector with RETRIEVAL_QUERY task type.
    2. Query official Pinecone Cloud index for top-k matching segments (Cosine similarity).
    3. Construct grounded prompt with citations.
    4. Call Gemini 2.5 Flash for hallucination-free generation.
    """
    print("\n🌲 Searching Pinecone vector index...")
    t0 = time.time()
    query_vector = client.embed_text(
        text=question,
        task_type="RETRIEVAL_QUERY",
        output_dim=db.dimension
    )
    results = db.search(query_vector, top_k=top_k)
    search_time = (time.time() - t0) * 1000

    if not results:
        print("⚠️  No relevant documents found in Pinecone index.")
        return

    print(f"⚡ Retrieved {len(results)} chunks in {search_time:.1f}ms:\n")
    for rank, (score, doc) in enumerate(results, 1):
        meta = doc.get("metadata", {})
        src = os.path.basename(meta.get("source", "unknown"))
        page = f", Page {meta['page']}" if "page" in meta else ""
        snippet = doc['text'][:120].replace('\n', ' ') + "..."
        print(f"  [{rank}] Score: {score:.4f} | Source: {src}{page}")
        print(f"      \"{snippet}\"")

    context_str = format_context(results)

    prompt = f"""You are a precise, reliable enterprise Q&A assistant.
Answer the user's question using ONLY the factual context provided below.
If the context does not contain enough information to answer the question accurately, explicitly state:
"I do not have enough information in the provided documentation to answer that question."
Do not make up facts or extrapolate beyond what is documented.

=== CONTEXT ===
{context_str}

=== QUESTION ===
{question}

=== ANSWER (Include citations to source numbers e.g. [Source #1] where applicable) ==="""

    print("\n🤖 Generating answer with Gemini 2.5 Flash...")
    t1 = time.time()
    answer = client.generate_answer(prompt, model="gemini-2.5-flash", temperature=0.1)
    gen_time = time.time() - t1

    print("\n" + "=" * 60)
    print("📢 ANSWER:")
    print("=" * 60)
    print(answer.strip())
    print("=" * 60)
    print(f"⏱️  Retrieval: {search_time:.1f}ms | Generation: {gen_time:.2f}s")

def main():
    try:
        client = GeminiClient()
    except ValueError as e:
        print(f"[CONFIGURATION ERROR] {e}")
        sys.exit(1)

    try:
        db = PineconeVectorDB(index_name="rag-bot", dimension=768)
    except ValueError as e:
        print(f"[PINECONE ERROR] {e}")
        sys.exit(1)

    if db.total_vectors == 0:
        print("\n[WARNING] Pinecone index currently has 0 vectors.")
        print("Please run ingestion first:")
        print("    python ingest.py docs/java_course.pdf")
        sys.exit(1)

    print("=" * 65)
    print("   🌲 PINECONE + GEMINI RAG CHAT CLI (Official Cloud Vector DB)")
    print(f"   Cloud Index: {db.index_name} | Total Vectors: {db.total_vectors}")
    print("   Commands: 'exit' or 'quit' to exit | 'stats' for index info")
    print("=" * 65)

    while True:
        try:
            user_input = input("\n💬 Ask a question: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye!")
                break

            if user_input.lower() == "stats":
                print(f"\n📊 Pinecone Cloud Stats:")
                print(f"   Index Name:   {db.index_name}")
                print(f"   Total Chunks: {db.total_vectors}")
                print(f"   Dimension:    {db.dimension}")
                print(f"   Metric:       Cosine Similarity")
                continue

            ask_question(user_input, client, db, top_k=3)

        except KeyboardInterrupt:
            print("\n👋 Session closed.")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()
