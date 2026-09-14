import os
import sys
import time
import argparse
import glob
import io
import pypdf
from chunking import RecursiveTextSplitter
from gemini_client import GeminiClient
from vector_db import PineconeVectorDB

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def extract_text_from_file(file_path: str, client: GeminiClient = None, progress_callback=None):
    """
    Reads document file and returns a list of (text_segment, metadata) tuples.
    For standard PDFs, extracts digital text layers.
    For scanned/image-based PDFs, automatically triggers Gemini Multimodal
    vision transcription and caches the extracted text locally.
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    base_name, ext = os.path.splitext(file_path)
    ext = ext.lower()

    segments = []
    if ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        segments.append((content, {"source": file_path, "type": "text"}))

    elif ext == ".pdf":
        print(f"📄 Extracting text from PDF: {file_path}...")
        cached_text_path = f"{base_name}.extracted.md"

        # If already extracted and cached, load from disk immediately
        if os.path.exists(cached_text_path):
            print(f"⚡ Found previously extracted text cache: {cached_text_path}. Loading...")
            if progress_callback:
                progress_callback(f"Loading cached OCR text for {os.path.basename(file_path)}...")
            with open(cached_text_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            segments.append((content, {"source": file_path, "type": "pdf_extracted"}))
            return segments

        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            total_pages = len(reader.pages)
            print(f"   Found {total_pages} pages.")

            total_chars = 0
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    total_chars += len(page_text)
                    segments.append((
                        page_text,
                        {"source": file_path, "page": page_num + 1, "type": "pdf"}
                    ))

            # If the PDF has almost no selectable text (scanned image slides), use Multimodal OCR
            if total_chars < 50 * max(1, total_pages):
                print("\n⚠️  Scanned/Image-based PDF detected (no digital text layer found).")
                print("🤖 Using Gemini Multimodal Vision to transcribe pages...")
                if client is None:
                    client = GeminiClient()

                segments = []
                all_extracted_text = []
                batch_size = 10

                for start_idx in range(0, total_pages, batch_size):
                    end_idx = min(start_idx + batch_size, total_pages)
                    status_msg = f"Transcribing pages {start_idx + 1} to {end_idx} of {total_pages} with Gemini Vision..."
                    print(f"   {status_msg}")
                    if progress_callback:
                        progress_callback(status_msg)

                    writer = pypdf.PdfWriter()
                    for p in reader.pages[start_idx:end_idx]:
                        writer.add_page(p)

                    pdf_buffer = io.BytesIO()
                    writer.write(pdf_buffer)
                    pdf_bytes = pdf_buffer.getvalue()

                    batch_text = client.extract_pdf_multimodal(
                        pdf_bytes,
                        instruction=(
                            f"Transcribe all text, code snippets, definitions, and notes from these pages "
                            f"(pages {start_idx + 1} to {end_idx}) accurately. "
                            f"Preserve all programming concepts, syntax, and hierarchy. Output clean Markdown."
                        )
                    )
                    all_extracted_text.append(batch_text)
                    segments.append((
                        batch_text,
                        {"source": file_path, "page_range": f"{start_idx + 1}-{end_idx}", "type": "pdf_multimodal"}
                    ))
                    # Polite pause between batches to protect free-tier rate limits
                    time.sleep(2)

                # Save cache so it doesn't need to be OCR'd again
                full_transcription = "\n\n".join(all_extracted_text)
                with open(cached_text_path, "w", encoding="utf-8") as f:
                    f.write(full_transcription)
                print(f"💾 Saved extracted text cache to: {cached_text_path}")

    else:
        print(f"[ERROR] Unsupported file extension '{ext}'. Only .txt, .md, and .pdf are supported.")
        sys.exit(1)

    return segments

def collect_target_files(file_patterns: list[str]) -> list[str]:
    """Expands file patterns and directories into valid file paths."""
    supported_exts = {".txt", ".pdf", ".md"}
    collected = []

    for pattern in file_patterns:
        if os.path.isdir(pattern):
            for root, _, files in os.walk(pattern):
                for f in files:
                    if os.path.splitext(f)[1].lower() in supported_exts:
                        collected.append(os.path.normpath(os.path.join(root, f)))
        else:
            matched = glob.glob(pattern)
            if matched:
                for path in matched:
                    if os.path.isfile(path) and os.path.splitext(path)[1].lower() in supported_exts:
                        collected.append(os.path.normpath(path))
            elif os.path.isfile(pattern):
                collected.append(os.path.normpath(pattern))
            else:
                print(f"[WARNING] Skipping '{pattern}' (file or directory not found).")

    # Deduplicate
    seen = set()
    unique = []
    for p in collected:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique

def ingest_documents(
    file_paths: list[str],
    clear_existing: bool = False,
    chunk_size: int = 700,
    chunk_overlap: int = 150
):
    """
    Ingests one or more documents into the official Pinecone vector database.
    """
    start_time = time.time()
    valid_files = collect_target_files(file_paths)

    if not valid_files:
        print("[ERROR] No valid .txt, .pdf, or .md files found to ingest.")
        return

    print("=" * 65)
    print(f"🌲 PINECONE INGESTION: {len(valid_files)} file(s) queued")
    for idx, f in enumerate(valid_files, 1):
        print(f"   [{idx}] {f}")
    print("=" * 65)

    # Initialize Gemini client & Pinecone Vector DB
    try:
        client = GeminiClient()
    except ValueError as e:
        print(f"[CONFIG ERROR] {e}")
        sys.exit(1)

    try:
        db = PineconeVectorDB(index_name="rag-bot", dimension=768)
    except ValueError as e:
        print(f"[PINECONE CONFIG ERROR] {e}")
        sys.exit(1)

    if clear_existing:
        print("🧹 Clearing previous vectors in Pinecone index...")
        db.clear()

    splitter = RecursiveTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_chunks = []
    all_metadatas = []

    # 1 & 2. Extract and Chunk each document
    print("\n[1/2] Extracting and chunking documents...")
    for f_idx, file_path in enumerate(valid_files, 1):
        file_name = os.path.basename(file_path)
        print(f"\n--- ({f_idx}/{len(valid_files)}) Processing '{file_name}' ---")
        segments = extract_text_from_file(file_path, client=client)
        if not segments:
            print(f"⚠️  No readable text in '{file_name}'. Skipping.")
            continue

        file_chunk_count = 0
        for seg_text, seg_meta in segments:
            chunks = splitter.split_text(seg_text)
            for chunk in chunks:
                meta = dict(seg_meta)
                meta["source"] = file_path
                meta["filename"] = file_name
                meta["chunk_index"] = len(all_chunks)
                meta["char_length"] = len(chunk)
                all_chunks.append(chunk)
                all_metadatas.append(meta)
                file_chunk_count += 1

        print(f"    Generated {file_chunk_count} chunks from '{file_name}'.")

    if not all_chunks:
        print("\n[ERROR] No chunks were generated from the input files.")
        return

    print(f"\n[2/2] Generating dense embeddings & upserting to Pinecone...")
    print(f"      Total new chunks to index: {len(all_chunks)}")

    # 3. Batch Embeddings & Pinecone Upsert
    batch_size = 25
    total_chunks = len(all_chunks)

    for i in range(0, total_chunks, batch_size):
        batch_chunks = all_chunks[i : i + batch_size]
        batch_meta = all_metadatas[i : i + batch_size]

        print(f"   Embedding & upserting chunks {i+1} to {min(i+batch_size, total_chunks)} of {total_chunks}...")
        embeddings = client.batch_embed_texts(
            texts=batch_chunks,
            task_type="RETRIEVAL_DOCUMENT",
            output_dim=768
        )

        db.add_documents(
            texts=batch_chunks,
            embeddings=embeddings,
            metadatas=batch_meta
        )

    elapsed = time.time() - start_time
    print("\n" + "=" * 65)
    print(f"✅ Ingestion successful in {elapsed:.2f}s!")
    print(f"   Indexed Files Count             : {len(valid_files)}")
    print(f"   New Chunks Upserted             : {len(all_chunks)}")
    print(f"   Pinecone Index                  : {db.index_name}")
    print(f"   Total Vectors in Pinecone Cloud : {db.total_vectors}")
    print(f"\nRun 'python query.py' to query your Pinecone vector database!")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest documents into the official Pinecone Vector Database."
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=["sample_doc.txt"],
        help="One or more files or folders to ingest (e.g. docs/java_course.pdf sample_doc.txt)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing vectors from Pinecone index before indexing",
    )
    args = parser.parse_args()

    ingest_documents(file_paths=args.files, clear_existing=args.clear)
