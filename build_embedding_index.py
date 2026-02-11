#!/usr/bin/env python3
"""
Build Embedding Index - Pre-compute embeddings for fast RAG
Run this ONCE to create embeddings index, then use opencode_rag_fast.py
"""

import json
import pickle
import requests
from pathlib import Path
from tqdm import tqdm

# Configuration
LM_STUDIO_URL = "http://localhost:1234"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v2-moe"
CORPUS_PATH = Path("/Users/jonathanmallinger/models/corpus_output.jsonl")
INDEX_PATH = Path("/Users/jonathanmallinger/models/embedding_index.pkl")

def get_embedding(text: str) -> list:
    """Get embedding vector for text"""
    response = requests.post(
        f"{LM_STUDIO_URL}/v1/embeddings",
        json={
            "model": EMBEDDING_MODEL,
            "input": text[:2000]  # Limit to 2000 chars
        },
        timeout=30
    )
    return response.json()["data"][0]["embedding"]

def build_index():
    """Build embedding index for all corpus documents"""
    print("=" * 60)
    print("Building Embedding Index")
    print("=" * 60)
    print(f"Corpus: {CORPUS_PATH}")
    print(f"Output: {INDEX_PATH}")
    print()

    # Load corpus
    docs = []
    with open(CORPUS_PATH) as f:
        for line in f:
            try:
                doc = json.loads(line)
                docs.append(doc)
            except:
                continue

    print(f"Loaded {len(docs)} documents")
    print()

    # Generate embeddings
    index = []
    print("Generating embeddings (this will take a few minutes)...")

    for i, doc in enumerate(tqdm(docs)):
        try:
            text = doc.get("text", "") or doc.get("content", "")
            if not text:
                continue

            embedding = get_embedding(text)

            index.append({
                "id": i,
                "text": text,
                "embedding": embedding,
                "metadata": {k: v for k, v in doc.items() if k not in ["text", "content"]}
            })
        except Exception as e:
            print(f"Error on doc {i}: {e}")
            continue

    # Save index
    print()
    print(f"Saving {len(index)} embeddings to {INDEX_PATH}...")
    with open(INDEX_PATH, 'wb') as f:
        pickle.dump(index, f)

    file_size_mb = INDEX_PATH.stat().st_size / 1024 / 1024
    print(f"✅ Index built: {file_size_mb:.2f} MB")
    print()
    print("Now use: ./opencode_rag_fast.py \"your question\"")

if __name__ == "__main__":
    build_index()
