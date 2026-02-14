# Models Project Context

## What This Project Is
Local MLX model management, MCP agent delegation, and RAG pipeline for M4 Pro Mac (24GB).
Working directory for LM Studio model configs, MCP servers, and retrieval scripts.

## Active Models (LM Studio)
- **Main model**: mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit (4.62 GB)
- **Upgrade models** (downloading):
  - mlx-community/Josiefied-Qwen3-30B-A3B-abliterated-v2-4bit (17.19 GB, abliterated, MoE 3B active)
  - lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-MLX-4bit (17.19 GB, coding-specialized)
- **Also available**: Josiefied-Qwen3-14B-abliterated-v3 (12.94 GB)
- **Draft model**: mlx-community/Josiefied-Qwen2.5-0.5B-abliterated (0.3 GB, for speculative decoding)
- **Embedding model**: nomic-embed-text-v2-moe (768-dim, 512 MB)
- **LM Studio API**: http://localhost:1234 (OpenAI-compatible)

## Speculative Decoding
- MUST load main model with `--parallel 1` (batched MLX breaks speculative decoding)
- 30B models + 0.5B draft = ~17.5 GB (fits in 24GB with ~6.5GB for KV cache + OS)
- 14B model + 0.5B draft = ~13.2 GB (comfortable fit)
- Green text in LM Studio = correctly predicted tokens from draft model

## MCP Local Agent Server
- **Server**: `mcp-local-agent/server.py` (delegates tasks to local LM Studio)
- **Tools**: local_analyze, local_summarize, local_research, local_embed, local_rag_query
- **Config**: `.mcp.json` has `local-agent` server registered
- **Venv**: `mcp-local-agent/.venv/` (python3, mcp 1.26.0, httpx 0.28.1)

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
