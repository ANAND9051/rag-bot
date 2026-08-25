import os
import json
import math

class SimpleVectorDB:
    def __init__(self, filepath="vector_db.json"):
        """
        A basic, file-based vector database.
        Stores chunks and embeddings in a JSON file and uses cosine similarity for search.
        """
        self.filepath = filepath
        self.data = []
        self.load()

    def load(self):
        """Loads data from the JSON file if it exists."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load database: {e}. Starting fresh.")
                self.data = []

    def save(self):
        """Saves current database state to the JSON file."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Failed to save database: {e}")

    def add(self, text, embedding, metadata=None):
        """Adds a document chunk, its embedding, and metadata, then saves it."""
        self.data.append({
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        })
        self.save()

    def query(self, query_embedding, n_results=2):
        """
        Computes cosine similarity between the query embedding and all stored embeddings.
        Returns the top `n_results` matching segments.
        """
        if not self.data:
            return []
            
        results = []
        for item in self.data:
            similarity = self.cosine_similarity(query_embedding, item["embedding"])
            results.append((similarity, item))
            
        # Sort results by similarity score descending (highest score first)
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:n_results]

    def cosine_similarity(self, v1, v2):
        """Calculates the cosine similarity between two numeric vectors."""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(a * a for a in v1))
        magnitude_v2 = math.sqrt(sum(a * a for a in v2))
        
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0.0
            
        return dot_product / (magnitude_v1 * magnitude_v2)
