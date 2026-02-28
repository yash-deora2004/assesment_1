"""
RAG Retriever — Queries the FAISS index and returns relevant chunks.
"""

import os
import numpy as np
from typing import List, Dict, Optional

from openai import OpenAI
import faiss

from rag.indexer import load_index, embed_texts, EMBEDDING_DIM, DEFAULT_INDEX_PATH

SIMILARITY_THRESHOLD = 0.3  # Minimum cosine similarity to consider a chunk relevant
DEFAULT_TOP_K = 5


class Retriever:
    """Retrieves relevant knowledge base chunks for a given query."""

    def __init__(self, index_path: str = DEFAULT_INDEX_PATH, client: OpenAI = None):
        self.client = client or OpenAI()
        self.index_path = index_path
        self._index = None
        self._chunks = None

    def _ensure_loaded(self):
        """Lazy-load the index."""
        if self._index is None:
            self._index, self._chunks = load_index(self.index_path)

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        topic_filter: Optional[str] = None,
    ) -> List[Dict]:
        """
        Retrieve the top-k most relevant chunks for a query.

        Args:
            query: The search query (parsed problem text).
            top_k: Number of top results to return.
            topic_filter: Optional topic to filter results (e.g., 'calculus').

        Returns:
            List of dicts with keys: text, metadata, score.
            Empty list if no chunk exceeds the similarity threshold.
        """
        self._ensure_loaded()

        # Embed the query
        query_embedding = embed_texts([query], self.client)
        faiss.normalize_L2(query_embedding)

        # Search the index (retrieve more if filtering by topic)
        search_k = top_k * 3 if topic_filter else top_k
        scores, indices = self._index.search(query_embedding, min(search_k, self._index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            if score < SIMILARITY_THRESHOLD:
                continue

            chunk = self._chunks[idx]

            # Apply topic filter
            if topic_filter and chunk["metadata"].get("topic") != topic_filter:
                continue

            results.append({
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "score": float(score),
            })

            if len(results) >= top_k:
                break

        return results

    def retrieve_with_sources(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        topic_filter: Optional[str] = None,
    ) -> Dict:
        """
        Retrieve chunks and format with source information.

        Returns:
            Dict with 'chunks' list and 'has_relevant_context' boolean.
        """
        chunks = self.retrieve(query, top_k, topic_filter)

        if not chunks:
            return {
                "chunks": [],
                "has_relevant_context": False,
                "message": "No relevant context found in the knowledge base.",
            }

        return {
            "chunks": chunks,
            "has_relevant_context": True,
            "sources": list(set(c["metadata"]["source_file"] for c in chunks)),
        }

    def format_context(self, chunks: List[Dict]) -> str:
        """Format retrieved chunks into a context string for the LLM."""
        if not chunks:
            return "No relevant context found in the knowledge base."

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk["metadata"]["source_file"]
            context_parts.append(
                f"[Source {i}: {source}]\n{chunk['text']}"
            )

        return "\n\n---\n\n".join(context_parts)
