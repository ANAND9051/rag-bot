import re
from typing import List

class RecursiveTextSplitter:
    """
    Recursively splits text using semantic boundaries (paragraphs, sentences, words)
    so chunks preserve coherent meaning without cutting words in half.
    """

    def __init__(
        self,
        chunk_size: int = 700,
        chunk_overlap: int = 150,
        separators: List[str] = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            return []
        return self._split(text, self.separators)

    def _split(self, text: str, separators: List[str]) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text] if text.strip() else []

        separator = ""
        next_separators = []
        for i, sep in enumerate(separators):
            if sep == "":
                separator = ""
                break
            if sep in text:
                separator = sep
                next_separators = separators[i + 1 :]
                break

        if separator:
            splits = text.split(separator)
        else:
            # Fallback character level
            splits = list(text)

        # Merge splits up to chunk_size with overlap
        chunks = []
        current_chunk = []
        current_length = 0

        for s in splits:
            s_len = len(s) + (len(separator) if current_chunk else 0)
            if current_length + s_len > self.chunk_size and current_chunk:
                merged = separator.join(current_chunk).strip()
                if merged:
                    chunks.append(merged)

                # Keep overlap pieces from the tail of current_chunk
                overlap_chunk = []
                overlap_len = 0
                for item in reversed(current_chunk):
                    item_len = len(item) + (len(separator) if overlap_chunk else 0)
                    if overlap_len + item_len <= self.chunk_overlap:
                        overlap_chunk.insert(0, item)
                        overlap_len += item_len
                    else:
                        break

                current_chunk = overlap_chunk
                current_length = overlap_len

            current_chunk.append(s)
            current_length += len(s) + (len(separator) if len(current_chunk) > 1 else 0)

        if current_chunk:
            merged = separator.join(current_chunk).strip()
            if merged:
                chunks.append(merged)

        # If any resulting chunk is still over chunk_size, split further with next_separators
        final_chunks = []
        for c in chunks:
            if len(c) > self.chunk_size and next_separators:
                sub_chunks = self._split(c, next_separators)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(c)

        return final_chunks
