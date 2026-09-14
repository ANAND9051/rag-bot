import os
import sys
import time
import tempfile
import streamlit as st
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables
load_dotenv()

from gemini_client import GeminiClient
from vector_db import PineconeVectorDB
from chunking import RecursiveTextSplitter
from ingest import extract_text_from_file

# --- Page Setup ---
st.set_page_config(
    page_title="Pinecone + Gemini RAG Assistant",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #e9ecef;
        margin-bottom: 8px;
    }
    .badge-score {
        background-color: #28a745;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .badge-source {
        background-color: #007bff;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    .stChatMessage {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Clients Initialization (Cached in Session) ---
@st.cache_resource
def get_gemini_client():
    return GeminiClient()

@st.cache_resource
def get_vector_db():
    return PineconeVectorDB(index_name="rag-bot", dimension=768)

try:
    client = get_gemini_client()
    db = get_vector_db()
    db_error = None
except Exception as e:
    client = None
    db = None
    db_error = str(e)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# --- Helper Functions ---
def format_context_for_llm(results):
    """Formats retrieved vector results into numbered context blocks."""
    blocks = []
    for rank, (score, doc) in enumerate(results, 1):
        meta = doc.get("metadata", {})
        source = os.path.basename(meta.get("source", "unknown"))
        page = f" (Page {meta['page']})" if "page" in meta else ""
        chunk_id = meta.get("chunk_index", doc.get("id"))
        header = f"[Source #{rank} | File: {source}{page} | Chunk: {chunk_id} | Cosine Score: {score:.4f}]"
        blocks.append(f"{header}\n{doc['text']}")
    return "\n\n".join(blocks)

def condense_query_with_history(query: str, history: list, client: GeminiClient) -> str:
    """Uses Gemini to formulate a standalone search query if conversational context is needed."""
    if not history or len(history) < 2:
        return query

    # Take the last 2 conversation turns
    recent_history = history[-4:]
    convo_summary = []
    for m in recent_history:
        role = "User" if m["role"] == "user" else "Assistant"
        # Truncate assistant responses for conciseness
        content = m["content"][:200].replace("\n", " ")
        convo_summary.append(f"{role}: {content}")
    history_text = "\n".join(convo_summary)

    prompt = f"""Given the chat history and follow-up question below, rephrase the follow-up question into a standalone, concise search query for a vector database.
Do NOT answer the question. Only return the standalone query.

Chat History:
{history_text}

Follow-up Question: {query}
Standalone Search Query:"""

    try:
        rephrased = client.generate_answer(prompt, model="gemini-2.5-flash", temperature=0.0).strip()
        # Clean quotes
        rephrased = rephrased.strip('"\'')
        return rephrased if rephrased else query
    except Exception:
        return query

def ingest_files_ui(uploaded_files, clear_existing: bool, chunk_size: int = 700, chunk_overlap: int = 150):
    """Processes uploaded files and updates the Pinecone index."""
    if not uploaded_files:
        st.warning("Please select at least one file to ingest.")
        return

    if clear_existing:
        with st.spinner("🧹 Clearing previous Pinecone index vectors..."):
            db.clear()
            st.success("Index cleared!")

    upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    progress_bar = st.progress(0, text="Starting ingestion...")
    status_text = st.empty()

    saved_file_paths = []
    for uploaded in uploaded_files:
        dest_path = os.path.join(upload_dir, uploaded.name)
        with open(dest_path, "wb") as f:
            f.write(uploaded.getbuffer())
        saved_file_paths.append(dest_path)

    splitter = RecursiveTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []
    all_metadatas = []

    total_files = len(saved_file_paths)
    for idx, path in enumerate(saved_file_paths, 1):
        filename = os.path.basename(path)
        status_text.text(f"Extracting & chunking ({idx}/{total_files}): {filename}")
        progress_bar.progress(int((idx / (total_files + 1)) * 40), text=f"Processing {filename}...")

        segments = extract_text_from_file(path, client=client)
        for seg_text, seg_meta in segments:
            chunks = splitter.split_text(seg_text)
            for chunk in chunks:
                meta = dict(seg_meta)
                meta["source"] = path
                meta["filename"] = filename
                meta["chunk_index"] = len(all_chunks)
                meta["char_length"] = len(chunk)
                all_chunks.append(chunk)
                all_metadatas.append(meta)

    if not all_chunks:
        st.error("No valid text could be extracted from the uploaded files.")
        return

    status_text.text(f"Generating embeddings for {len(all_chunks)} chunks...")
    batch_size = 25
    total_chunks = len(all_chunks)

    for i in range(0, total_chunks, batch_size):
        batch_chunks = all_chunks[i : i + batch_size]
        batch_meta = all_metadatas[i : i + batch_size]

        pct = 40 + int(((i + len(batch_chunks)) / total_chunks) * 55)
        progress_bar.progress(min(pct, 98), text=f"Upserting vectors {i+1}-{min(i+batch_size, total_chunks)} to Pinecone...")

        embeddings = client.batch_embed_texts(
            texts=batch_chunks,
            task_type="RETRIEVAL_DOCUMENT",
            output_dim=768
        )
        db.add_documents(texts=batch_chunks, embeddings=embeddings, metadatas=batch_meta)

    progress_bar.progress(100, text="Ingestion complete!")
    status_text.success(f" Successfully indexed {len(all_chunks)} chunks across {total_files} file(s) into Pinecone!")
    time.sleep(1.5)
    st.rerun()

# --- Sidebar UI ---
with st.sidebar:
    st.title("🌲 Pinecone Cloud")
    st.caption("Official Cloud Vector Database")

    if db_error:
        st.error(f"⚠️ Configuration Error: {db_error}")
        st.info("Check your `.env` file for `PINECONE_API_KEY` and `GEMINI_API_KEY`.")
    else:
        # Live vector count & status
        vector_count = db.total_vectors
        st.markdown(
            f"""
            <div class="metric-card">
                <div><strong>Index:</strong> <code>{db.index_name}</code></div>
                <div><strong>Status:</strong> <span style="color:#28a745;">● Connected</span></div>
                <div><strong>Cloud Spec:</strong> AWS us-east-1 (Serverless)</div>
                <div><strong>Dimension:</strong> {db.dimension} | <strong>Metric:</strong> Cosine</div>
                <div><strong>Total Live Vectors:</strong> <span style="font-size:1.1rem; font-weight:bold; color:#007bff;">{vector_count}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Document Ingestion Section
    st.subheader("📤 Document Ingestion")
    uploaded_files = st.file_uploader(
        "Upload PDF, TXT, or MD documents",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        help="Supports digital PDFs, scanned PDFs (via Gemini Multimodal OCR), and plain text.",
    )

    clear_before = st.checkbox("Clear index before ingesting", value=False)

    if st.button("🚀 Ingest to Pinecone", use_container_width=True, disabled=(db is None)):
        if uploaded_files:
            ingest_files_ui(uploaded_files, clear_existing=clear_before)
        else:
            st.warning("Please upload files first.")

    with st.expander("🛠️ Index Management"):
        if st.button("🧹 Clear Entire Pinecone Index", type="secondary", use_container_width=True):
            if db:
                db.clear()
                st.success("Pinecone index cleared!")
                time.sleep(1)
                st.rerun()

    st.divider()

    # RAG Settings Section
    st.subheader("⚙️ Query Configuration")
    top_k = st.slider("Top-K Chunks to Retrieve", min_value=1, max_value=8, value=3)
    temperature = st.slider("Generation Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
    model_choice = st.selectbox("Gemini Model", ["gemini-2.5-flash", "gemini-2.5-pro"], index=0)
    enable_chat_memory = st.checkbox("Enable Conversational Memory", value=True, help="Rephrases follow-up questions using past turns to maintain context.")

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main Chat UI ---
st.title("Document Q&A Assistant")
st.markdown("Ask questions grounded strictly on documents indexed in **Pinecone Cloud** powered by **Google Gemini**.")

# Quick Questions / Sample prompts if chat is empty
if not st.session_state.messages and db and db.total_vectors > 0:
    st.markdown("##### 💡 Try asking:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Java Flavours", use_container_width=True):
            st.session_state.quick_prompt = "What are the flavours of Java?"
            st.rerun()
    with col2:
        if st.button("Why Learn Java?", use_container_width=True):
            st.session_state.quick_prompt = "Why learn Java according to the course?"
            st.rerun()
    with col3:
        if st.button("Compilation Process", use_container_width=True):
            st.session_state.quick_prompt = "What is the compilation and execution process in Java?"
            st.rerun()
    with col4:
        if st.button("Hallucination Test", use_container_width=True):
            st.session_state.quick_prompt = "What is the weather in Tokyo?"
            st.rerun()

# Render existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            metrics = msg.get("metrics", {})
            retrieval_ms = metrics.get("retrieval_ms", 0)
            gen_s = metrics.get("generation_s", 0)
            with st.expander(f"📚 View Retrieved Sources ({len(msg['sources'])} chunks | ⚡ Retrieval: {retrieval_ms:.1f}ms | ⏱️ Generation: {gen_s:.2f}s)"):
                for rank, (score, doc) in enumerate(msg["sources"], 1):
                    meta = doc.get("metadata", {})
                    src = os.path.basename(meta.get("source", "unknown"))
                    page = f" (Page {meta['page']})" if "page" in meta else ""
                    st.markdown(
                        f"**Source #{rank}** | `{src}{page}` | Similarity: `{score:.4f}`"
                    )
                    st.text(doc.get("text", ""))

# Determine user input (from chat input or quick button)
user_query = st.chat_input("Ask a question about your documents...")
if st.session_state.quick_prompt:
    user_query = st.session_state.quick_prompt
    st.session_state.quick_prompt = None

if user_query:
    if not db or db.total_vectors == 0:
        st.warning("⚠️ No documents are currently indexed in Pinecone. Please upload and ingest a document first via the sidebar!")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Assistant response container
        with st.chat_message("assistant"):
            # 1. Conversational Query Formulation (if enabled)
            search_query = user_query
            if enable_chat_memory and len(st.session_state.messages) > 1:
                with st.spinner("🧠 Understanding context..."):
                    search_query = condense_query_with_history(user_query, st.session_state.messages[:-1], client)

            # 2. Dense Vector Retrieval from Pinecone
            t0 = time.time()
            with st.spinner("🌲 Searching Pinecone vector index..."):
                query_vector = client.embed_text(
                    text=search_query,
                    task_type="RETRIEVAL_QUERY",
                    output_dim=db.dimension,
                )
                retrieved_results = db.search(query_vector, top_k=top_k)
            retrieval_time_ms = (time.time() - t0) * 1000

            if not retrieved_results:
                no_context_resp = "I could not find any relevant information in the uploaded documents."
                st.markdown(no_context_resp)
                st.session_state.messages.append({"role": "assistant", "content": no_context_resp})
            else:
                context_str = format_context_for_llm(retrieved_results)

                # Format conversation history for LLM
                history_prompt_parts = []
                if enable_chat_memory:
                    for prev_msg in st.session_state.messages[-5:-1]:
                        speaker = "User" if prev_msg["role"] == "user" else "Assistant"
                        history_prompt_parts.append(f"{speaker}: {prev_msg['content']}")
                history_block = "\n".join(history_prompt_parts)

                prompt = f"""You are a precise, reliable enterprise Q&A assistant.
Answer the user's question using ONLY the factual context provided below.
If the context does not contain enough information to answer the question accurately, explicitly state:
"I do not have enough information in the provided documentation to answer that question."
Do not make up facts, extrapolate, or hallucinate beyond what is documented.

=== RECENT CONVERSATION ===
{history_block if history_block else "None"}

=== FACTUAL CONTEXT FROM PINECONE ===
{context_str}

=== USER QUESTION ===
{user_query}

=== GROUNDED ANSWER (Cite source numbers e.g. [Source #1] where applicable) ==="""

                # 3. Live Streaming Generation
                t1 = time.time()
                stream_generator = client.generate_answer_stream(
                    prompt=prompt,
                    model=model_choice,
                    temperature=temperature,
                )

                response_placeholder = st.empty()
                full_response = response_placeholder.write_stream(stream_generator)
                gen_time_s = time.time() - t1

                # 4. Show Source Expander
                with st.expander(f"📚 View Retrieved Sources ({len(retrieved_results)} chunks | ⚡ Retrieval: {retrieval_time_ms:.1f}ms | ⏱️ Generation: {gen_time_s:.2f}s)"):
                    for rank, (score, doc) in enumerate(retrieved_results, 1):
                        meta = doc.get("metadata", {})
                        src = os.path.basename(meta.get("source", "unknown"))
                        page = f" (Page {meta['page']})" if "page" in meta else ""
                        st.markdown(
                            f"**Source #{rank}** | `{src}{page}` | Similarity: `{score:.4f}`"
                        )
                        st.text(doc.get("text", ""))

                # Save message to session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "sources": retrieved_results,
                    "metrics": {
                        "retrieval_ms": retrieval_time_ms,
                        "generation_s": gen_time_s,
                    },
                })
