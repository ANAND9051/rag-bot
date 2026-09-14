import os
import time
import uuid
from typing import List, Dict, Tuple, Any, Optional
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

class PineconeVectorDB:
    """
    Official Cloud Vector Database backed by Pinecone (Serverless).
    Provides persistent cloud vector storage, cosine similarity search,
    and metadata filtering with global low-latency availability.
    """

    def __init__(
        self,
        index_name: str = "rag-bot",
        dimension: int = 768,
        metric: str = "cosine",
        cloud: str = "aws",
        region: str = "us-east-1",
        api_key: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("PINECONE_API_KEY")
        if not self.api_key or self.api_key.startswith("YOUR_"):
            raise ValueError(
                "PINECONE_API_KEY is not set. Please set it in your .env file or pass it to PineconeVectorDB."
            )

        self.index_name = index_name
        self.dimension = dimension
        self.metric = metric

        # Initialize official Pinecone client
        self.pc = Pinecone(api_key=self.api_key)

        # Ensure index exists
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            print(f"📦 Creating serverless Pinecone index '{self.index_name}'...")
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric=self.metric,
                spec=ServerlessSpec(cloud=cloud, region=region),
            )
            # Wait until index is ready
            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)

        self.index = self.pc.Index(self.index_name)

    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        batch_size: int = 50,
    ) -> int:
        """
        Upserts document chunks and embeddings with metadata to Pinecone.
        """
        if not texts or not embeddings:
            return 0

        if len(texts) != len(embeddings):
            raise ValueError("Number of texts must match number of embeddings.")

        if metadatas is None:
            metadatas = [{} for _ in texts]

        vectors_to_upsert = []
        for idx, (text, emb, meta) in enumerate(zip(texts, embeddings, metadatas)):
            # Create a clean, deterministic or unique ID
            src_file = os.path.basename(meta.get("source", "doc"))
            chunk_num = meta.get("chunk_index", idx)
            vector_id = f"{src_file}_chunk_{chunk_num}_{uuid.uuid4().hex[:6]}"

            # Store the chunk text directly in Pinecone metadata
            payload_meta = dict(meta)
            payload_meta["text"] = text

            vectors_to_upsert.append({
                "id": vector_id,
                "values": emb,
                "metadata": payload_meta,
            })

        # Batch upsert to Pinecone
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i : i + batch_size]
            self.index.upsert(vectors=batch)

        return len(texts)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3,
        score_threshold: Optional[float] = None,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Queries Pinecone for the top-k most similar chunks.
        Returns a list of tuples: (similarity_score, document_info).
        """
        query_res = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
        )

        results = []
        matches = getattr(query_res, "matches", []) or []

        for match in matches:
            score = float(match.score)
            if score_threshold is not None and score < score_threshold:
                continue

            metadata = match.metadata or {}
            doc_text = metadata.get("text", "")

            doc_info = {
                "id": match.id,
                "text": doc_text,
                "metadata": metadata,
            }
            results.append((score, doc_info))

        return results

    def clear(self):
        """Deletes all vectors from the Pinecone index."""
        try:
            self.index.delete(delete_all=True)
            # Give Pinecone cloud a moment to propagate deletion
            time.sleep(1)
        except Exception as e:
            # If index is already empty, delete(delete_all=True) might return 404 or empty
            pass

    @property
    def total_vectors(self) -> int:
        """Returns the number of vectors stored in the Pinecone index."""
        try:
            stats = self.index.describe_index_stats()
            return stats.total_vector_count or 0
        except Exception:
            return 0
