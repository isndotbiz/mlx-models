#!/usr/bin/env python3
"""
MCP server that delegates analysis, summarization, research, embedding,
and RAG tasks to a local LM Studio instance.

LM Studio exposes an OpenAI-compatible API at http://localhost:1234.
Chat model : Josiefied-Qwen3-14B-abliterated-v3
Embedding model: nomic-embed-text-v2-moe (768-dim)
RAG backend: pgvector (PostgreSQL)
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

import httpx
import psycopg2
import psycopg2.extras
from mcp.server.fastmcp import FastMCP
from pgvector.psycopg2 import register_vector

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_BASE_URL", "http://localhost:1234")
CHAT_MODEL = os.environ.get(
    "LM_STUDIO_CHAT_MODEL",
    "josiefied-qwen3-14b-abliterated-v3",
)
EMBEDDING_MODEL = os.environ.get(
    "LM_STUDIO_EMBEDDING_MODEL",
    "nomic-embed-text-v2-moe",
)
PG_DSN = os.environ.get("PG_DSN", "postgresql://localhost/rag_db")

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
# pgvector RAG helpers
# ---------------------------------------------------------------------------


def _pgvector_query(query_embedding: list[float], top_k: int) -> list[dict]:
    """Query the security_corpus table using cosine similarity."""
    conn = psycopg2.connect(PG_DSN)
    register_vector(conn)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    content,
                    source_file,
                    technique_id,
                    slug,
                    source_repo,
                    chunk_id,
                    total_chunks,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM security_corpus
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                [query_embedding, query_embedding, top_k],
            )
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "local-agent",
    instructions=(
        "Delegates analysis, summarization, research, embedding, and RAG "
        "tasks to a local LM Studio instance (Qwen3-14B). Use this to offload "
        "work and save Claude tokens."
    ),
)


# -- Tool: local_analyze ----------------------------------------------------


@mcp.tool()
def local_analyze(file_path: str, prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
    """Read a file and analyze it with the local LLM. Use for code review, bug hunting, or documentation tasks."""
    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return f"Error: File not found: {path}"
    if not path.is_file():
        return f"Error: Path is not a file: {path}"

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
    """Summarize text with the local LLM. style: "concise" (bullets), "detailed" (paragraphs), or "technical"."""
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
    """Answer a research question using the local LLM's training knowledge. Provide context to ground the response."""
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
    """Generate 768-dim embeddings via nomic-embed-text-v2-moe. Returns {"embeddings", "dimensions", "count", "model"}."""
    if isinstance(text, str):
        texts = [text]
    else:
        texts = list(text)

    if not texts:
        return {"error": "No text provided."}

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
    """Query pgvector RAG (security-research corpus, 1447 docs) and answer with grounded LLM response. Returns {"answer", "sources", "chunks_used"}."""
    # Step 1: Embed the question via LM Studio (same model used at ingest time)
    try:
        query_embedding = _get_embeddings([question])[0]
    except (ConnectionError, TimeoutError, RuntimeError) as exc:
        return {"error": f"Embedding failed: {exc}"}

    # Step 2: Query pgvector with the pre-computed embedding vector
    try:
        rows = _pgvector_query(query_embedding, top_k)
    except Exception as exc:
        return {"error": f"pgvector query failed: {exc}"}

    if not rows:
        return {"error": "No chunks retrieved from pgvector."}

    # Step 3: Build context from retrieved chunks
    context_parts = []
    for i, row in enumerate(rows, 1):
        source = row.get("source_file", "unknown")
        score = row.get("similarity", 0.0)
        context_parts.append(
            f"--- Chunk {i} (source: {source}, relevance: {score:.3f}) ---\n"
            f"{row['content']}\n"
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

    # Build source list
    sources = []
    for row in rows:
        sources.append({
            "score": round(float(row.get("similarity", 0.0)), 3),
            "source_file": row.get("source_file", "unknown"),
            "text_preview": row["content"][:200] + ("..." if len(row["content"]) > 200 else ""),
        })

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(rows),
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
    log.info("pgvector DSN  : %s", PG_DSN)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
