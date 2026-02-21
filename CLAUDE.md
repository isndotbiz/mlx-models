# Models Project Context

## What This Project Is
Local MLX model management, MCP agent delegation, and RAG pipeline for M4 Pro Mac (24GB).
Working directory for LM Studio model configs, MCP servers, and retrieval scripts.

## Active Models (LM Studio - port 1234)
- **Josiefied-Qwen3-14B-abliterated-v3**: 12.94 GB (primary model, best quality/size for 24GB)
- **Josiefied-Qwen3-8B-abliterated-v1-4bit**: 4.62 GB (lighter tasks)
- **Draft model**: Josiefied-Qwen2.5-0.5B-abliterated (0.3 GB, speculative decoding for 14B)
- **Embedding**: nomic-embed-text-v2-moe (768-dim, 512 MB)
- LM Studio API: http://localhost:1234

## Speculative Decoding (LM Studio)
- MUST load main model with `--parallel 1` (batched MLX breaks speculative decoding)
- 14B model + 0.5B draft = ~13.2 GB (comfortable fit in 24GB, ~11 GB free)

## MCP Local Agent Server
- **Server**: `mcp-local-agent/server.py` (delegates tasks to local models)
- **Tools**: local_analyze, local_summarize, local_research, local_embed, local_rag_query
- **Config**: `.mcp.json` routes to LM Studio (port 1234, 14B model)
- **RAG**: local_rag_query uses pgvector (PostgreSQL) — `PG_DSN=postgresql://localhost/rag_db`
- **Venv**: `mcp-local-agent/.venv/` (python3.12, mcp, httpx, psycopg2-binary, pgvector)

## RAG System
- **Location**: ~/workspace/rag-system/ (separated, own GitHub repo: isndotbiz/rag-system)
- **Storage**: pgvector — PostgreSQL `rag_db` database, `security_corpus` table (768-dim, ivfflat index)
- **Ingestion**: `ingest_security_corpus.py --pg-dsn postgresql://localhost/rag_db` (venv python3.12)
- **Query**: `query_rag.py "your query"` (uses $PG_DSN or postgresql://localhost/rag_db by default)
- **Source data**: `corpus_output.jsonl` (3.4 MB, 1,447 chunks from 137 security research files)
- **MCP integration**: mcp-local-agent/server.py queries pgvector directly for RAG queries
- **PostgreSQL**: brew postgresql@17, running on :5432 (brew services start postgresql@17)

## MLX Server (mlx-server/) - ARCHIVED
- Was used to serve 30B MoE models that LM Studio couldn't detect (qwen3_moe arch not supported)
- 30B models deleted — too large for 24GB machine (16.4 GB RAM, left only ~5 GB free)
- Code kept for reference in case LM Studio adds qwen3_moe support or larger RAM becomes available

## Related Projects
- `~/workspace/llm-security-research/` - Main security research project (source of corpus data)
- `~/workspace/rag-system/` - Full RAG pipeline (GitHub: isndotbiz/rag-system)

## Token Optimization
- Superpowers plugin: DISABLED (~22K tokens saved per session)
- Serena: ~6-7K tokens (active, useful for code navigation + memories)
- Compound-engineering: ~5-6K tokens (active, context7 docs)
- GitHub MCP: available but disabled at user level

## Future Upgrades Identified
- cc_token_saver_mcp (additional Claude-to-local delegation)
- Qwen3-Embedding-0.6B (alternative to nomic, 44K tok/s on MLX)
- Add hybrid BM25+vector search via pg_trgm or a full-text tsvector column
