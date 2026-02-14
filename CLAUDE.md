# Models Project Context

## What This Project Is
Local MLX model management, MCP agent delegation, and RAG pipeline for M4 Pro Mac (24GB).
Working directory for LM Studio model configs, MCP servers, and retrieval scripts.

## Active Models

### 30B Models (MLX Server - port 8080)
- **josiefied-qwen3-30b-a3b-abliterated**: Josiefied-Qwen3-30B-A3B-abliterated-v2-4bit (16 GB, abliterated MoE, 3B active/token)
- **qwen3-coder-30b-a3b**: Qwen3-Coder-30B-A3B-Instruct-MLX-4bit (16 GB, coding-specialized MoE)
- Served via `mlx-server/server.py` on http://localhost:8080 (OpenAI-compatible)
- Start: `./mlx-server/start.sh` (or `--model qwen3-coder-30b-a3b` for coder)
- LM Studio 0.4.2 does NOT support qwen3_moe arch yet - must use mlx_lm direct server

### LM Studio Models (port 1234)
- **Josiefied-Qwen3-8B-abliterated-v1-4bit**: 4.62 GB (smaller tasks, LM Studio)
- **Josiefied-Qwen3-14B-abliterated-v3**: 12.94 GB (mid-range, LM Studio)
- **Draft model**: Josiefied-Qwen2.5-0.5B-abliterated (0.3 GB, speculative decoding)
- **Embedding**: nomic-embed-text-v2-moe (768-dim, 512 MB)
- LM Studio API: http://localhost:1234

## MLX Server (mlx-server/)
- **Server**: `mlx-server/server.py` - OpenAI-compatible API for 30B MoE models via mlx_lm 0.30.7
- **Venv**: `mlx-server/.venv/` (python3.12, mlx-lm, fastapi, uvicorn)
- **Start**: `./mlx-server/start.sh` (default: abliterated model, port 8080, no-thinking)
- **Flags**: `--model`, `--port`, `--thinking` (enable reasoning mode), `--no-thinking` (default)
- **Endpoints**: `/v1/chat/completions`, `/v1/models`, `/health`
- **Why**: LM Studio 0.4.2 scanner doesn't recognize qwen3_moe architecture

## Speculative Decoding (LM Studio only)
- MUST load main model with `--parallel 1` (batched MLX breaks speculative decoding)
- 14B model + 0.5B draft = ~13.2 GB (comfortable fit in 24GB)
- Not available for 30B models via MLX server (would need mlx_lm draft model support)

## MCP Local Agent Server
- **Server**: `mcp-local-agent/server.py` (delegates tasks to local models)
- **Tools**: local_analyze, local_summarize, local_research, local_embed, local_rag_query
- **Config**: `.mcp.json` routes to MLX server (port 8080, 30B model) by default
- **Venv**: `mcp-local-agent/.venv/` (python3, mcp 1.26.0, httpx 0.28.1)
- **To use LM Studio 8B instead**: set env `LM_STUDIO_BASE_URL=http://localhost:1234`

## RAG System
- **Location**: ~/workspace/rag-system/ (separated, own GitHub repo: isndotbiz/rag-system)
- **Storage**: ChromaDB at ~/workspace/rag-system/chroma_data/ (1,447 docs, security_corpus collection)
- **Ingestion**: `ingest_security_corpus.py` (use python3.12, NOT python3.14 due to pydantic v1 issue)
- **Query**: `query_rag.py --mode chromadb --collection-name security_corpus`
- **Source data**: `corpus_output.jsonl` (3.4 MB, 1,447 chunks from 137 security research files)
- **Old embedding_index.pkl**: DELETED (all data migrated to ChromaDB RAG)

## Related Projects
- `~/workspace/llm-security-research/` - Main security research project (source of corpus data)
- `~/workspace/rag-system/` - Full RAG pipeline (GitHub: isndotbiz/rag-system)

## Token Optimization
- Superpowers plugin: DISABLED (~22K tokens saved per session)
- Serena: ~6-7K tokens (active, useful for code navigation + memories)
- Compound-engineering: ~5-6K tokens (active, context7 docs)
- GitHub MCP: available but disabled at user level

## Future Upgrades Identified
- LanceDB over ChromaDB (native hybrid search, zero config, better performance)
- mcp-local-rag by shinpr (MCP RAG server with LanceDB)
- cc_token_saver_mcp (additional Claude-to-local delegation)
- Qwen3-Embedding-0.6B (alternative to nomic, 44K tok/s on MLX)
