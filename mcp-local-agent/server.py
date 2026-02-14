#!/usr/bin/env python3
"""
MCP server that delegates analysis, summarization, research, embedding,
and RAG tasks to a local LM Studio instance.

LM Studio exposes an OpenAI-compatible API at http://localhost:1234.
Chat model : Josiefied-Qwen3-8B-abliterated-v1-4bit
Embedding model: nomic-embed-text-v2-moe (768-dim)
"""

from __future__ import annotations

import logging
import os
import pickle
import sys
from pathlib import Path
from typing import Any

import httpx
import numpy as np
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_BASE_URL", "http://localhost:1234")
CHAT_MODEL = os.environ.get(
    "LM_STUDIO_CHAT_MODEL",
    "Josiefied-Qwen3-8B-abliterated-v1-4bit",
)
EMBEDDING_MODEL = os.environ.get(
    "LM_STUDIO_EMBEDDING_MODEL",
    "nomic-embed-text-v2-moe",
)
EMBEDDING_INDEX_PATH = os.environ.get(
    "EMBEDDING_INDEX_PATH",
    "/Users/jonathanmallinger/models/embedding_index.pkl",
)

REQUEST_TIMEOUT = float(os.environ.get("LM_STUDIO_TIMEOUT", "120"))
DEFAULT_MAX_TOKENS = int(os.environ.get("LM_STUDIO_MAX_TOKENS", "4096"))
DEFAULT_TEMPERATURE = float(os.environ.get("LM_STUDIO_TEMPERATURE", "0.7"))
RAG_TOP_K = int(os.environ.get("RAG_TOP_K", "8"))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("mcp-local-agent")

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _http_client() -> httpx.Client:
    """Return a reusable synchronous httpx client with appropriate timeout."""
    return httpx.Client(
        base_url=LM_STUDIO_BASE_URL,
        timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=10.0),
    )


def _chat_completion(
    messages: list[dict[str, str]],
    *,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> str:
    """Call LM Studio chat completions endpoint and return the assistant text."""
    payload: dict[str, Any] = {
        "model": CHAT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    try:
        with _http_client() as client:
            resp = client.post("/v1/chat/completions", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except httpx.ConnectError:
        raise ConnectionError(
            f"Cannot connect to LM Studio at {LM_STUDIO_BASE_URL}. "
            "Is LM Studio running with the local server enabled?"
        )
    except httpx.TimeoutException:
        raise TimeoutError(
            f"LM Studio request timed out after {REQUEST_TIMEOUT}s. "
            "The model may be overloaded or the prompt too large."
        )
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"LM Studio returned HTTP {exc.response.status_code}: "
            f"{exc.response.text[:500]}"
        )


def _get_embeddings(texts: list[str]) -> list[list[float]]:
    """Call LM Studio embeddings endpoint and return embedding vectors."""
    payload: dict[str, Any] = {
        "model": EMBEDDING_MODEL,
        "input": texts,
    }
    try:
        with _http_client() as client:
            resp = client.post("/v1/embeddings", json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Sort by index to guarantee order matches input order
            sorted_items = sorted(data["data"], key=lambda d: d["index"])
            return [item["embedding"] for item in sorted_items]
    except httpx.ConnectError:
        raise ConnectionError(
            f"Cannot connect to LM Studio at {LM_STUDIO_BASE_URL}. "
            "Is LM Studio running with the local server enabled?"
        )
    except httpx.TimeoutException:
        raise TimeoutError(
            f"LM Studio embedding request timed out after {REQUEST_TIMEOUT}s."
        )
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"LM Studio returned HTTP {exc.response.status_code}: "
            f"{exc.response.text[:500]}"
        )


# ---------------------------------------------------------------------------
# RAG index helpers
# ---------------------------------------------------------------------------

_rag_index_cache: dict[str, Any] | None = None


def _load_rag_index() -> list[dict[str, Any]]:
    """Load and cache the embedding index from disk."""
    global _rag_index_cache  # noqa: PLW0603
    if _rag_index_cache is not None:
        return _rag_index_cache

    index_path = Path(EMBEDDING_INDEX_PATH)
    if not index_path.exists():
        raise FileNotFoundError(
            f"Embedding index not found at {EMBEDDING_INDEX_PATH}. "
            "Run the index builder first."
        )
    log.info("Loading RAG index from %s ...", EMBEDDING_INDEX_PATH)
    with open(index_path, "rb") as fh:
        _rag_index_cache = pickle.load(fh)  # noqa: S301
    log.info("Loaded %d chunks into RAG index.", len(_rag_index_cache))
    return _rag_index_cache


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between vector *a* and matrix *b* (rows)."""
    a_norm = a / (np.linalg.norm(a) + 1e-10)
    b_norms = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-10)
    return b_norms @ a_norm


def _retrieve_chunks(query_embedding: list[float], top_k: int = RAG_TOP_K) -> list[dict[str, Any]]:
    """Return top-k most similar chunks from the RAG index."""
    index = _load_rag_index()
    embeddings_matrix = np.array([entry["embedding"] for entry in index], dtype=np.float32)
    query_vec = np.array(query_embedding, dtype=np.float32)
    similarities = _cosine_similarity(query_vec, embeddings_matrix)
    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = []
    for idx in top_indices:
        entry = index[int(idx)]
        results.append({
            "id": entry.get("id"),
            "text": entry["text"],
            "score": float(similarities[idx]),
            "metadata": entry.get("metadata", {}),
        })
    return results


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "local-agent",
    instructions=(
        "Delegates analysis, summarization, research, embedding, and RAG "
        "tasks to a local LM Studio instance (Qwen3-8B). Use this to offload "
        "work and save Claude tokens."
    ),
)


# -- Tool: local_analyze ----------------------------------------------------


@mcp.tool()
def local_analyze(file_path: str, prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
    """
    Read a file from disk and send it along with a prompt to the local LLM
    for analysis. Useful for code review, bug hunting, documentation
    generation, or any per-file analysis task.

    Args:
        file_path: Absolute path to the file to analyze.
        prompt: Instructions for the analysis (e.g. "Find bugs in this code").
        max_tokens: Maximum tokens for the response (default 4096).

    Returns:
        The local LLM's analysis of the file.
    """
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {path}"
    if not path.is_file():
        return f"Error: Path is not a file: {path}"

    # Guard against enormous files
    file_size = path.stat().st_size
    if file_size > 500_000:
        return (
            f"Error: File is too large ({file_size:,} bytes). "
            "Consider splitting it or summarizing specific sections."
        )

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"Error reading file: {exc}"

    # Determine a reasonable file-type hint
    suffix = path.suffix.lstrip(".")
    lang_hint = suffix if suffix else "text"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a meticulous analyst. The user will provide a file "
                "and an instruction. Analyze the file carefully and respond "
                "with a well-structured answer."
            ),
        },
        {
            "role": "user",
            "content": (
                f"**File**: `{path.name}` ({lang_hint})\n\n"
                f"```{lang_hint}\n{content}\n```\n\n"
                f"**Task**: {prompt}"
            ),
        },
    ]

    try:
        return _chat_completion(messages, max_tokens=max_tokens, temperature=0.3)
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return f"Error: {exc}"


# -- Tool: local_summarize --------------------------------------------------


@mcp.tool()
def local_summarize(
    content: str,
    style: str = "concise",
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Summarize text content using the local LLM. Supports different styles:
    concise (bullet points), detailed (paragraph), or technical (preserves
    jargon and specifics).

    Args:
        content: The text to summarize.
        style: One of "concise", "detailed", or "technical" (default "concise").
        max_tokens: Maximum tokens for the response (default 4096).

    Returns:
        A summary of the provided content.
    """
    style_instructions = {
        "concise": (
            "Provide a concise summary using bullet points. "
            "Capture the key points only."
        ),
        "detailed": (
            "Provide a detailed summary in well-structured paragraphs. "
            "Preserve important nuances and context."
        ),
        "technical": (
            "Provide a technical summary that preserves domain-specific "
            "terminology, code references, and precise details."
        ),
    }

    instruction = style_instructions.get(
        style,
        style_instructions["concise"],
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert summarizer. Follow the user's style "
                "instruction precisely."
            ),
        },
        {
            "role": "user",
            "content": f"**Style instruction**: {instruction}\n\n**Content to summarize**:\n\n{content}",
        },
    ]

    try:
        return _chat_completion(messages, max_tokens=max_tokens, temperature=0.4)
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return f"Error: {exc}"


# -- Tool: local_research ---------------------------------------------------


@mcp.tool()
def local_research(
    question: str,
    context: str = "",
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """
    Ask the local LLM a research question. It answers from its training
    knowledge. Optionally provide context to ground the response.

    Args:
        question: The research question to answer.
        context: Optional additional context or constraints for the answer.
        max_tokens: Maximum tokens for the response (default 4096).

    Returns:
        The local LLM's answer to the research question.
    """
    user_content = question
    if context:
        user_content = f"**Context**:\n{context}\n\n**Question**: {question}"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a knowledgeable research assistant. Answer the "
                "user's question thoroughly and accurately. If you are "
                "uncertain about something, say so clearly. Structure your "
                "answer with headings and bullet points where appropriate."
            ),
        },
        {"role": "user", "content": user_content},
    ]

    try:
        return _chat_completion(messages, max_tokens=max_tokens, temperature=0.7)
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return f"Error: {exc}"


# -- Tool: local_embed ------------------------------------------------------


@mcp.tool()
def local_embed(text: str | list[str]) -> dict:
    """
    Generate embeddings for one or more texts via the local embedding model
    (nomic-embed-text-v2-moe, 768-dim).

    Args:
        text: A single string or a list of strings to embed.

    Returns:
        A dict with "embeddings" (list of float vectors) and "dimensions".
    """
    if isinstance(text, str):
        texts = [text]
    else:
        texts = list(text)

    if not texts:
        return {"error": "No text provided."}

    # Guard against excessive batch size
    if len(texts) > 100:
        return {"error": "Too many texts. Maximum batch size is 100."}

    try:
        embeddings = _get_embeddings(texts)
        return {
            "embeddings": embeddings,
            "dimensions": len(embeddings[0]) if embeddings else 0,
            "count": len(embeddings),
            "model": EMBEDDING_MODEL,
        }
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return {"error": str(exc)}


# -- Tool: local_rag_query --------------------------------------------------


@mcp.tool()
def local_rag_query(
    question: str,
    top_k: int = RAG_TOP_K,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> dict:
    """
    Query the local RAG index. Computes the query embedding, retrieves the
    top-k most similar chunks, then sends those chunks and the question to
    the local LLM for a grounded answer.

    The index is loaded from /Users/jonathanmallinger/models/embedding_index.pkl.

    Args:
        question: The question to answer using RAG.
        top_k: Number of similar chunks to retrieve (default 8).
        max_tokens: Maximum tokens for the LLM response (default 4096).

    Returns:
        A dict with "answer", "sources" (retrieved chunks with scores),
        and "chunks_used".
    """
    # Step 1: Compute query embedding
    try:
        query_embeddings = _get_embeddings([question])
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return {"error": f"Embedding failed: {exc}"}

    query_embedding = query_embeddings[0]

    # Step 2: Retrieve top-k similar chunks
    try:
        chunks = _retrieve_chunks(query_embedding, top_k=top_k)
    except FileNotFoundError as exc:
        return {"error": str(exc)}

    if not chunks:
        return {"error": "No chunks retrieved from the index."}

    # Step 3: Build context from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source_file", "unknown")
        score = chunk["score"]
        context_parts.append(
            f"--- Chunk {i} (source: {source}, relevance: {score:.3f}) ---\n"
            f"{chunk['text']}\n"
        )
    context_block = "\n".join(context_parts)

    # Step 4: Send to LLM for grounded answer
    messages = [
        {
            "role": "system",
            "content": (
                "You are a precise research assistant. Answer the user's "
                "question using ONLY the provided context chunks. "
                "Cite the chunk numbers when referencing information. "
                "If the context does not contain enough information to answer "
                "the question, say so explicitly."
            ),
        },
        {
            "role": "user",
            "content": (
                f"**Retrieved Context**:\n\n{context_block}\n\n"
                f"**Question**: {question}"
            ),
        },
    ]

    try:
        answer = _chat_completion(messages, max_tokens=max_tokens, temperature=0.3)
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return {"error": f"LLM call failed: {exc}"}

    # Build source list (without the full embedding vectors)
    sources = []
    for chunk in chunks:
        sources.append({
            "id": chunk.get("id"),
            "score": chunk["score"],
            "source_file": chunk.get("metadata", {}).get("source_file", "unknown"),
            "text_preview": chunk["text"][:200] + ("..." if len(chunk["text"]) > 200 else ""),
        })

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks),
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main():
    """Run the MCP server via stdio transport."""
    log.info("Starting mcp-local-agent server...")
    log.info("LM Studio URL : %s", LM_STUDIO_BASE_URL)
    log.info("Chat model    : %s", CHAT_MODEL)
    log.info("Embed model   : %s", EMBEDDING_MODEL)
    log.info("RAG index     : %s", EMBEDDING_INDEX_PATH)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
