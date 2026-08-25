import os
import sys
import pypdf
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

# Initialize our custom Vector DB (saves to vector_db.json)
db = SimpleVectorDB()

def extract_text_from_file(file_path):
    """
    Reads the file path and extracts text. Supports .txt and .pdf formats.
    """
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)
        
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        print(f"Extracting text from PDF: {file_path}...")
        text = ""
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    else:
        print(f"[ERROR] Unsupported file extension '{ext}'. Only .txt and .pdf are supported.")
        sys.exit(1)

def chunk_text(text, chunk_size=700, overlap=150):
    """
    Splits text into chunks of length `chunk_size` with `overlap` characters.
    Overlapping ensures that context is preserved at the chunk boundary.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        # Move the start pointer forward, leaving `overlap` characters behind
        start += chunk_size - overlap
    return chunks

def embed_text(text_chunk):
    """
    Generates semantic vector embeddings using Gemini's text-embedding-004 model.
    Returns a list of floats (the embedding vector).
    """
    try:
        response = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text_chunk,
            task_type="retrieval_document"
        )
        return response['embedding']
    except Exception as e:
        print(f"[ERROR] Embedding generation failed: {e}")
        sys.exit(1)

def ingest_document(file_path):
    """
    Reads, chunks, embeds, and stores the document into our vector database.
    """
    print(f"1. Reading document from '{file_path}'...")
    raw_text = extract_text_from_file(file_path)
    
    print("2. Splitting text into chunks...")
    chunks = chunk_text(raw_text)
    print(f"   Created {len(chunks)} chunks.")
    
    print("3. Generating embeddings & storing in database...")
    for idx, chunk in enumerate(chunks):
        # Generate the embedding vector for the current chunk
        embedding = embed_text(chunk)
        
        # Add to custom vector DB
        db.add(
            text=chunk,
            embedding=embedding,
            metadata={"source": file_path, "chunk_index": idx}
        )
        print(f"   Indexed chunk {idx+1}/{len(chunks)}")
        
    print("\n[SUCCESS] Ingestion completed. Run 'query.py' to ask questions about your documents!")

if __name__ == "__main__":
    # If a file path is provided as a command line argument, use it; otherwise use sample_doc.txt
    target_file = "sample_doc.txt"
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    ingest_document(target_file)
