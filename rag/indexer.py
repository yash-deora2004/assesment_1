"""
RAG Indexer — Chunks markdown docs, embeds them, and builds a FAISS index.
"""

import os
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
import faiss

KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
DEFAULT_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", os.path.join("data", "faiss_index"))
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents(kb_dir: str = KNOWLEDGE_BASE_DIR) -> List:
    """Load all markdown documents from the knowledge base directory."""
    loader = DirectoryLoader(
        kb_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    return loader.load()


def chunk_documents(documents: List, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Dict]:
    """Split documents into smaller chunks with metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )

    chunks = []
    for doc in documents:
        source_file = os.path.basename(doc.metadata.get("source", "unknown"))
        topic = _infer_topic(source_file)
        splits = splitter.split_text(doc.page_content)
        for i, text in enumerate(splits):
            chunks.append({
                "text": text,
                "metadata": {
                    "source_file": source_file,
                    "topic": topic,
                    "chunk_index": i,
                },
            })
    return chunks


def _infer_topic(filename: str) -> str:
    """Infer the topic from the filename."""
    name = filename.replace(".md", "")
    if name.startswith("algebra"):
        return "algebra"
    elif name.startswith("prob"):
        return "probability"
    elif name.startswith("calc"):
        return "calculus"
    elif name.startswith("linalg"):
        return "linear_algebra"
    elif name.startswith("trig"):
        return "trigonometry"
    else:
        return "general"


def embed_texts(texts: List[str], client: OpenAI = None) -> np.ndarray:
    """Embed a list of texts using OpenAI embeddings API."""
    if client is None:
        client = OpenAI()

    # Process in batches of 100 (API limit is 2048, but 100 is safe)
    all_embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch,
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

    return np.array(all_embeddings, dtype="float32")


def build_index(chunks: List[Dict], client: OpenAI = None) -> tuple:
    """Build a FAISS index from chunks."""
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts, client)

    # Build FAISS index (L2 distance — we normalize for cosine similarity)
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)  # Inner product after normalization = cosine similarity
    index.add(embeddings)

    return index, chunks


def save_index(index: faiss.Index, chunks: List[Dict], index_path: str = DEFAULT_INDEX_PATH):
    """Save FAISS index and chunk metadata to disk."""
    os.makedirs(index_path, exist_ok=True)
    faiss.write_index(index, os.path.join(index_path, "index.faiss"))

    metadata_path = os.path.join(index_path, "chunks.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Index saved to {index_path} ({index.ntotal} vectors)")


def load_index(index_path: str = DEFAULT_INDEX_PATH) -> tuple:
    """Load FAISS index and chunk metadata from disk."""
    index = faiss.read_index(os.path.join(index_path, "index.faiss"))

    metadata_path = os.path.join(index_path, "chunks.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return index, chunks


def build_and_save(kb_dir: str = KNOWLEDGE_BASE_DIR, index_path: str = DEFAULT_INDEX_PATH):
    """Full pipeline: load docs → chunk → embed → build index → save."""
    print("Loading documents...")
    documents = load_documents(kb_dir)
    print(f"Loaded {len(documents)} documents")

    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and building FAISS index...")
    client = OpenAI()
    index, chunks = build_index(chunks, client)

    print("Saving index...")
    save_index(index, chunks, index_path)

    return index, chunks


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    build_and_save()
