# Local AI Infrastructure Deep Dive Manual

**Author**: Jonathan Mallinger
**Last Updated**: 2026-02-15
**Platforms**: macOS (M4 Pro 24GB), Windows (RTX 3090 24GB), NAS (16GB + 24GB GPUs)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Mac Setup (M4 Pro 24GB) — Complete Reference](#mac-setup)
3. [RAG System — Deep Dive](#rag-system)
4. [MCP Agent — Tool Reference](#mcp-agent)
5. [OpenCode Integration](#opencode-integration)
6. [Windows Setup (RTX 3090 24GB)](#windows-setup)
7. [NAS Setup (16GB + 24GB GPUs)](#nas-setup)
8. [Syncing Everything via GitHub](#syncing-via-github)
9. [Quick Reference Card](#quick-reference)

---

## 1. Architecture Overview <a name="architecture-overview"></a>

```
                    ┌─────────────────┐
                    │   Claude Code   │  (Anthropic API)
                    │   / OpenCode    │
                    └────────┬────────┘
                             │ MCP Protocol
                    ┌────────▼────────┐
                    │  MCP Local Agent │  (mcp-local-agent/server.py)
                    │  5 Tools:        │
                    │  - local_analyze │
                    │  - local_summarize│
                    │  - local_research│
                    │  - local_embed   │
                    │  - local_rag_query│
                    └───┬─────────┬───┘
                        │         │
               ┌────────▼──┐  ┌──▼────────┐
               │ LM Studio │  │  ChromaDB  │
               │ Port 1234  │  │  1,447 docs│
               │ 14B + Spec │  │  Security  │
               │ Decoding   │  │  Corpus    │
               └────────────┘  └───────────┘
```

**How it saves tokens**: When Claude Code calls `local_rag_query` or `local_research`, the heavy lifting (embedding search, text generation) happens on your local GPU. Claude only pays for the MCP tool call overhead, not the actual inference.

---

## 2. Mac Setup (M4 Pro 24GB) — Complete Reference <a name="mac-setup"></a>

### What's Installed

| Component | Location | Purpose |
|-----------|----------|---------|
| LM Studio 0.4.2 | /Applications/LM Studio.app | Model inference server |
| MCP Local Agent | ~/models/mcp-local-agent/ | MCP tool server |
| RAG System | ~/workspace/rag-system/ | ChromaDB + ingestion pipeline |
| MLX Server | ~/models/mlx-server/ | ARCHIVED (was for 30B models) |
| OpenCode 1.1.50 | /opt/homebrew/bin/opencode | Local coding assistant |

### Models on Disk (11 models, 30.8 GB)

| Model | Size | Use |
|-------|------|-----|
| **Josiefied-Qwen3-14B-abliterated-v3** | 12.94 GB | **PRIMARY** — best quality for 24GB |
| Josiefied-Qwen3-8B-abliterated-v1 | 4.62 GB | Lighter alternative |
| Josiefied-Qwen2.5-0.5B-abliterated | 294 MB | Speculative decoding draft model |
| nomic-embed-text-v2-moe | 512 MB | Embedding model (optional for RAG) |
| DeepSeek-R1-Distill-Qwen-1.5B | 789 MB | Reasoning model |
| Gemma-3-4B-abliterated | 2.6 GB | Google model |
| Josiefied-Qwen2.5-3B | 1.75 GB | Small Qwen |
| Josiefied-Qwen3-1.7B | 984 MB | Tiny Qwen |
| Mistral-7B | 4.08 GB | Mistral |
| Qwen3-4B | 2.15 GB | Small Qwen3 |

### Starting Everything (Mac)

```bash
# 1. Open LM Studio (GUI app)

# 2. Load the 14B model with speculative decoding via CLI
lms load josiefied-qwen3-14b-abliterated-v3 --parallel 1 -y

# 3. Enable speculative decoding in LM Studio UI:
#    - Click loaded model → Settings → Speculative Decoding → ON
#    - Draft model: Josiefied-Qwen2.5-0.5B-abliterated

# 4. Verify it's working
curl -s http://localhost:1234/v1/models | python3 -m json.tool
curl -s http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"josiefied-qwen3-14b-abliterated-v3","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'
```

### Memory Budget (24GB)

| Component | RAM | Notes |
|-----------|-----|-------|
| macOS + apps | ~4 GB | Browser, IDE, etc. |
| 14B model | ~13 GB | Primary model |
| 0.5B draft | ~0.3 GB | Speculative decoding |
| ChromaDB | ~0.5 GB | In-process when queried |
| **Free** | **~6 GB** | Comfortable headroom |

### Key Config Files

| File | Purpose |
|------|---------|
| `~/models/.mcp.json` | MCP server config for ~/models/ projects |
| `~/workspace/llm-security-research/.mcp.json` | MCP config for security research |
| `~/models/mcp-local-agent/server.py` | MCP agent server code |
| `~/models/CLAUDE.md` | Claude Code project context |

---

## 3. RAG System — Deep Dive <a name="rag-system"></a>

### What's In the Corpus

- **1,447 chunks** from 137 security research files
- Topics: jailbreak techniques, prompt injection, identity manipulation, model attacks
- Source: `~/workspace/llm-security-research/` → processed into `corpus_output.jsonl`
- Stored in: ChromaDB at `~/workspace/rag-system/chroma_data/`
- Collection: `security_corpus` (also duplicated as `security-research`)

### Embeddings

The corpus uses **ChromaDB's built-in all-MiniLM-L6-v2** (384 dimensions). This means:
- RAG queries do NOT need an external embedding model
- nomic-embed-text-v2-moe is NOT required for RAG
- Queries work even if LM Studio has no embedding model loaded

### Command-Line RAG Queries

```bash
cd ~/workspace/rag-system

# ──────────────────────────────────────────────
# RETRIEVAL ONLY (no LLM needed, instant results)
# ──────────────────────────────────────────────

# Basic search — returns top 5 matching chunks
python3.12 query_rag.py "jailbreak techniques" \
  --mode chromadb --collection-name security_corpus

# More results
python3.12 query_rag.py "prompt injection via roleplay" \
  --mode chromadb --collection-name security_corpus --top-k 10

# Filter by source repository
python3.12 query_rag.py "identity manipulation" \
  --mode chromadb --collection-name security_corpus \
  --filter-repo spiritual-spell

# ──────────────────────────────────────────────
# RAG (retrieval + LM Studio generates answer)
# Requires LM Studio running with a model loaded
# ──────────────────────────────────────────────

# Basic RAG query
python3.12 query_rag.py "What are the main categories of jailbreak techniques?" \
  --mode chromadb --collection-name security_corpus --generate

# Deep dive with more context
python3.12 query_rag.py "ENI LIME jailbreak technique details" \
  --mode chromadb --collection-name security_corpus --generate --top-k 10

# Claude-specific attacks
python3.12 query_rag.py "techniques that specifically target Claude" \
  --mode chromadb --collection-name security_corpus --generate --top-k 10

# Defense research
python3.12 query_rag.py "defenses against prompt injection" \
  --mode chromadb --collection-name security_corpus --generate

# Cross-model comparison
python3.12 query_rag.py "differences between GPT and Claude jailbreaks" \
  --mode chromadb --collection-name security_corpus --generate

# DAN jailbreak family
python3.12 query_rag.py "DAN jailbreak evolution and variants" \
  --mode chromadb --collection-name security_corpus --generate --top-k 10

# Chain of thought attacks
python3.12 query_rag.py "chain of thought and chain of draft attacks" \
  --mode chromadb --collection-name security_corpus --generate

# Grok-specific techniques
python3.12 query_rag.py "Grok jailbreak techniques" \
  --mode chromadb --collection-name security_corpus --generate
```

### RAG via Claude Code (MCP)

When using Claude Code in `~/models/` or `~/workspace/llm-security-research/`:

```
You: "Search the RAG for DAN jailbreak techniques"
Claude: [calls local_rag_query MCP tool → ChromaDB search → 14B generates answer]
Result: Grounded answer citing chunk sources, zero Claude tokens on inference

You: "What does our corpus say about Claude API jailbreaks?"
Claude: [calls local_rag_query]

You: "Summarize the top techniques for identity manipulation"
Claude: [calls local_rag_query with high top_k]
```

### Adding New Data to the Corpus

```bash
cd ~/workspace/rag-system

# 1. Add new .md files to ~/workspace/llm-security-research/

# 2. Re-process into JSONL
cd ~/models
python3.12 process_to_jsonl.py

# 3. Re-ingest into ChromaDB (idempotent — won't duplicate existing docs)
cd ~/workspace/rag-system
python3.12 ingest_security_corpus.py \
  --input ~/models/corpus_output.jsonl \
  --mode chromadb \
  --collection-name security_corpus

# IMPORTANT: Use python3.12, NOT python3.14 (pydantic v1 incompatibility)
```

---

## 4. MCP Agent — Tool Reference <a name="mcp-agent"></a>

The MCP local-agent server exposes 5 tools that Claude Code can call:

### local_rag_query
**Purpose**: Search security corpus and get grounded answer
```
Input:  question="How do chain-of-draft jailbreaks work?"
        top_k=8 (default)
        max_tokens=4096 (default)
Output: { answer: "...", sources: [...], chunks_used: 8 }
```

### local_analyze
**Purpose**: Send a file to the local LLM for analysis
```
Input:  file_path="/path/to/code.py"
        prompt="Find security vulnerabilities in this code"
Output: LLM's analysis of the file
```

### local_summarize
**Purpose**: Summarize text locally
```
Input:  content="long text..."
        style="concise" | "detailed" | "technical"
Output: Summary in requested style
```

### local_research
**Purpose**: Ask the local LLM a knowledge question
```
Input:  question="What is prompt injection?"
        context="optional additional context"
Output: LLM's answer from training knowledge
```

### local_embed
**Purpose**: Generate embedding vectors
```
Input:  text="some text" or ["text1", "text2"]
Output: { embeddings: [[...]], dimensions: 768 }
```
Note: Requires nomic-embed-text-v2-moe loaded in LM Studio.

---

## 5. OpenCode Integration <a name="opencode-integration"></a>

### Using OpenCode with LM Studio

```bash
cd ~/workspace/llm-security-research
opencode
# Select LM Studio as provider
# Endpoint: http://localhost:1234
# Model: josiefied-qwen3-14b-abliterated-v3
```

OpenCode talks directly to LM Studio's API. No Claude tokens used. Good for:
- Code review and generation
- Quick questions
- Interactive coding sessions

### Using Claude Code with Local Delegation

```bash
cd ~/workspace/llm-security-research
claude
# Claude Code connects, MCP local-agent available
# Ask Claude to delegate to local model for cheaper tasks
```

---

## 6. Windows Setup (RTX 3090 24GB) <a name="windows-setup"></a>

### Why It's Different

| | Mac (M4 Pro) | Windows (3090) |
|--|--------------|----------------|
| Memory | Unified 24GB (shared CPU/GPU) | 24GB dedicated VRAM + system RAM |
| Format | MLX (Apple Silicon native) | GPTQ/AWQ/GGUF (CUDA) |
| Server | LM Studio | vLLM or Ollama |
| Speed | ~18 tok/s (14B) | ~40-80 tok/s (14B, CUDA) |

The 3090 has **dedicated** 24GB VRAM, so you can run larger models without affecting system performance. You can comfortably run a 14B or even 30B quantized model.

### Software to Install

#### Option A: vLLM (Recommended — fastest, production-grade)

**GitHub**: https://github.com/vllm-project/vllm

```powershell
# Requires: Python 3.10-3.12, CUDA 12.x, PyTorch 2.x
pip install vllm

# Start server (OpenAI-compatible API, same as LM Studio)
vllm serve Qwen/Qwen3-14B-AWQ \
  --quantization awq \
  --max-model-len 8192 \
  --port 1234 \
  --gpu-memory-utilization 0.9

# Or for 30B MoE (fits in 24GB VRAM with AWQ):
vllm serve Qwen/Qwen3-30B-A3B-Instruct-AWQ \
  --quantization awq \
  --max-model-len 8192 \
  --port 1234

# Speculative decoding with vLLM:
vllm serve Qwen/Qwen3-14B-AWQ \
  --quantization awq \
  --speculative-model Qwen/Qwen2.5-0.5B \
  --num-speculative-tokens 5 \
  --port 1234
```

#### Option B: Ollama (Simpler, cross-platform)

**GitHub**: https://github.com/ollama/ollama
**Download**: https://ollama.com/download/windows

```powershell
# Install from website, then:
ollama pull qwen3:14b
ollama serve
# API at http://localhost:11434 (OpenAI-compatible at /v1/)

# Or for abliterated models, create a Modelfile:
# FROM qwen3:14b
# PARAMETER temperature 0.7
ollama create my-qwen3-14b -f Modelfile
```

#### Option C: LM Studio (Same as Mac, GUI)

**Download**: https://lmstudio.ai
- Works on Windows with CUDA
- Same UI, same workflow as Mac
- Download GGUF versions of the same models

### Models for Windows (CUDA-optimized)

| Model | Format | HuggingFace Repo | VRAM |
|-------|--------|-------------------|------|
| Qwen3-14B | AWQ 4-bit | `Qwen/Qwen3-14B-AWQ` | ~10 GB |
| Qwen3-30B-A3B | AWQ 4-bit | `Qwen/Qwen3-30B-A3B-Instruct-AWQ` | ~18 GB |
| Qwen3-Coder-30B-A3B | AWQ 4-bit | `Qwen/Qwen3-Coder-30B-A3B-Instruct-AWQ` | ~18 GB |
| Qwen2.5-0.5B | FP16 | `Qwen/Qwen2.5-0.5B-Instruct` | ~1 GB |

For abliterated/uncensored versions, search HuggingFace for:
- `Josiefied-Qwen3-14B-abliterated` + GPTQ or AWQ
- **HuggingFace**: https://huggingface.co/models?search=josiefied+qwen3+abliterated

### Windows Step-by-Step

```powershell
# 1. Install prerequisites
#    - Python 3.12: https://python.org
#    - CUDA Toolkit 12.x: https://developer.nvidia.com/cuda-downloads
#    - Git: https://git-scm.com

# 2. Clone your repos
git clone https://github.com/isndotbiz/mlx-models.git models
git clone https://github.com/isndotbiz/rag-system.git rag-system

# 3. Set up MCP local-agent
cd models\mcp-local-agent
python -m venv .venv
.venv\Scripts\activate
pip install mcp httpx chromadb

# 4. Set up RAG system
cd ..\..\rag-system
python -m venv .venv
.venv\Scripts\activate
pip install chromadb

# 5. Copy corpus data (sync via GitHub or manual transfer)
# The chroma_data/ directory needs to be copied or re-ingested

# 6. Install vLLM
pip install vllm

# 7. Download model
# vLLM auto-downloads from HuggingFace on first run, or:
huggingface-cli download Qwen/Qwen3-14B-AWQ

# 8. Start vLLM server
vllm serve Qwen/Qwen3-14B-AWQ --quantization awq --port 1234

# 9. Update .mcp.json to point at localhost:1234
# (same config, just change model name to match vLLM)

# 10. Test
curl http://localhost:1234/v1/models
curl -X POST http://localhost:1234/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"Qwen/Qwen3-14B-AWQ\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}"
```

### GitHub Repos Needed for Windows

| Repo | URL | Purpose |
|------|-----|---------|
| vLLM | https://github.com/vllm-project/vllm | CUDA inference server |
| Ollama | https://github.com/ollama/ollama | Alternative inference (simpler) |
| ChromaDB | https://github.com/chroma-core/chroma | Vector database for RAG |
| MCP Python SDK | https://github.com/modelcontextprotocol/python-sdk | MCP server framework |
| OpenCode | https://github.com/opencode-ai/opencode | Local coding assistant |
| Your models repo | https://github.com/isndotbiz/mlx-models | Config + MCP agent code |
| Your RAG repo | https://github.com/isndotbiz/rag-system | RAG pipeline + ChromaDB data |
| HuggingFace CLI | `pip install huggingface-hub` | Model downloads |

---

## 7. NAS Setup (16GB + 24GB GPUs) <a name="nas-setup"></a>

### Architecture

The NAS serves as a **central inference server** for your network. All devices (Mac, Windows, phone) can send API requests to it.

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│   Mac    │    │ Windows  │    │  Phone   │
│ Claude   │    │ OpenCode │    │  App     │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     └───────────────┼───────────────┘
                     │ HTTP API
              ┌──────▼──────┐
              │     NAS     │
              │ vLLM/Ollama │
              │ 16GB + 24GB │
              │   GPUs      │
              └─────────────┘
```

### Docker Deployment (Recommended)

**GitHub**: https://github.com/vllm-project/vllm (Docker images included)

```yaml
# docker-compose.yml for NAS
version: '3.8'

services:
  # Main inference server (24GB GPU)
  vllm-main:
    image: vllm/vllm-openai:latest
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=0  # 24GB GPU
    ports:
      - "1234:8000"
    volumes:
      - ./models:/root/.cache/huggingface
    command: >
      --model Qwen/Qwen3-14B-AWQ
      --quantization awq
      --max-model-len 8192
      --gpu-memory-utilization 0.9
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # Secondary server (16GB GPU) — smaller model or embeddings
  vllm-secondary:
    image: vllm/vllm-openai:latest
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=1  # 16GB GPU
    ports:
      - "1235:8000"
    volumes:
      - ./models:/root/.cache/huggingface
    command: >
      --model Qwen/Qwen3-8B-AWQ
      --quantization awq
      --max-model-len 8192
      --gpu-memory-utilization 0.9

  # ChromaDB server (CPU, persistent storage)
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_data:/chroma/chroma
    environment:
      - ANONYMIZED_TELEMETRY=False

  # Ollama alternative (simpler, supports multiple models)
  # ollama:
  #   image: ollama/ollama:latest
  #   runtime: nvidia
  #   ports:
  #     - "11434:11434"
  #   volumes:
  #     - ./ollama_data:/root/.ollama
```

### NAS Models by GPU Size

**24GB GPU** (can run same models as 3090):
| Model | Format | VRAM |
|-------|--------|------|
| Qwen3-30B-A3B-Instruct-AWQ | AWQ 4-bit | ~18 GB |
| Qwen3-14B-AWQ | AWQ 4-bit | ~10 GB |
| Qwen3-Coder-30B-A3B-AWQ | AWQ 4-bit | ~18 GB |

**16GB GPU**:
| Model | Format | VRAM |
|-------|--------|------|
| Qwen3-14B-AWQ | AWQ 4-bit | ~10 GB |
| Qwen3-8B | FP16 or AWQ | ~5-10 GB |
| nomic-embed-text-v2 | FP16 | ~0.5 GB |

### Multi-GPU Strategy

Best setup for your NAS:
1. **24GB GPU**: Run the largest/best model (30B-A3B or 14B)
2. **16GB GPU**: Run embeddings + smaller model for speculative decoding or lighter tasks
3. **ChromaDB**: Runs on CPU, store on SSD

### Connecting Mac/Windows to NAS

Update `.mcp.json` on any machine to point at the NAS:

```json
{
  "mcpServers": {
    "local-agent": {
      "type": "stdio",
      "command": "python3",
      "args": ["path/to/mcp-local-agent/server.py"],
      "env": {
        "LM_STUDIO_BASE_URL": "http://NAS_IP:1234",
        "LM_STUDIO_CHAT_MODEL": "Qwen/Qwen3-14B-AWQ",
        "CHROMADB_PATH": "/path/to/chroma_data",
        "CHROMADB_COLLECTION": "security_corpus"
      }
    }
  }
}
```

Or if running ChromaDB on the NAS too, modify the MCP agent to use ChromaDB's HTTP client instead of PersistentClient:
```python
# Change from:
client = chromadb.PersistentClient(path=CHROMADB_PATH)
# To:
client = chromadb.HttpClient(host="NAS_IP", port=8000)
```

### NAS Prerequisites

| Software | URL | Purpose |
|----------|-----|---------|
| Docker | https://docs.docker.com/engine/install/ | Container runtime |
| NVIDIA Container Toolkit | https://github.com/NVIDIA/nvidia-container-toolkit | GPU passthrough to Docker |
| nvidia-smi | Included with NVIDIA drivers | Verify GPU access |

---

## 8. Syncing Everything via GitHub <a name="syncing-via-github"></a>

### Repos to Keep in Sync

| Repo | GitHub | Contains |
|------|--------|----------|
| `mlx-models` | isndotbiz/mlx-models | MCP agent, configs, scripts, this manual |
| `rag-system` | isndotbiz/rag-system | RAG pipeline, ChromaDB data, ingestion scripts |
| `llm-security-research` | isndotbiz/llm-security-research | Source corpus, research files |

### What Syncs via Git (small files)

- MCP agent code (`mcp-local-agent/server.py`)
- Config files (`.mcp.json`, `CLAUDE.md`)
- Scripts and presets
- RAG ingestion scripts
- This manual

### What Does NOT Sync (too large)

- Model weights (download fresh on each machine)
- ChromaDB data directory (re-ingest from corpus_output.jsonl)
- Python venvs (recreate per machine)

### Setting Up a New Machine

```bash
# 1. Clone repos
git clone https://github.com/isndotbiz/mlx-models.git models
git clone https://github.com/isndotbiz/rag-system.git rag-system
git clone https://github.com/isndotbiz/llm-security-research.git

# 2. Set up MCP agent venv
cd models/mcp-local-agent
python3.12 -m venv .venv
.venv/bin/pip install mcp httpx chromadb  # Linux/Mac
# .venv\Scripts\pip install mcp httpx chromadb  # Windows

# 3. Set up RAG and ingest corpus
cd ../../rag-system
python3.12 -m venv .venv
.venv/bin/pip install chromadb
python3.12 ingest_security_corpus.py \
  --input ../models/corpus_output.jsonl \
  --mode chromadb \
  --collection-name security_corpus

# 4. Install inference server
# Mac: LM Studio (https://lmstudio.ai)
# Windows: pip install vllm (or Ollama)
# NAS: docker-compose up -d

# 5. Download models
# Mac: lms get <model> (or via LM Studio GUI)
# Windows: huggingface-cli download Qwen/Qwen3-14B-AWQ
# NAS: vLLM auto-downloads on first run

# 6. Update .mcp.json with correct model name and port
```

---

## 9. Quick Reference Card <a name="quick-reference"></a>

### Start Everything (Mac)

```bash
# Open LM Studio, then:
lms load josiefied-qwen3-14b-abliterated-v3 --parallel 1 -y
# Enable speculative decoding in UI (draft: 0.5B)
```

### Test Everything

```bash
# LM Studio API
curl -s http://localhost:1234/v1/models | python3 -m json.tool

# Chat test
curl -s http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"josiefied-qwen3-14b-abliterated-v3","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'

# RAG test (retrieval only)
cd ~/workspace/rag-system
python3.12 query_rag.py "jailbreak" --mode chromadb --collection-name security_corpus

# RAG test (with LLM answer)
python3.12 query_rag.py "jailbreak" --mode chromadb --collection-name security_corpus --generate

# MCP agent test
cd ~/models
claude  # Claude Code picks up .mcp.json automatically
# Ask: "Use local_rag_query to search for DAN jailbreaks"
```

### Ports

| Service | Port | Machine |
|---------|------|---------|
| LM Studio | 1234 | Mac |
| vLLM main | 1234 | Windows / NAS |
| vLLM secondary | 1235 | NAS (16GB GPU) |
| ChromaDB HTTP | 8000 | NAS |
| MLX Server | 8080 | Mac (ARCHIVED) |

### Python Version Rules

| Task | Python Version | Why |
|------|---------------|-----|
| MCP agent | 3.12 | ChromaDB + pydantic v1 breaks on 3.14 |
| RAG ingestion | 3.12 | Same pydantic issue |
| MLX server | 3.12 | mlx-lm requirement |
| Everything else | Any | No restrictions |

### Troubleshooting

| Problem | Fix |
|---------|-----|
| LM Studio not responding | Check if model is loaded: `lms ps` |
| RAG returns no results | Verify collection: `python3.12 -c "import chromadb; c=chromadb.PersistentClient(path='./chroma_data'); print(c.get_collection('security_corpus').count())"` |
| "pydantic v1 incompatible" | You're using Python 3.14. Switch to 3.12. |
| Speculative decoding slow | Verify `--parallel 1` was set: `lms ps` should show loaded model |
| MCP tool not found | Restart Claude Code to reload `.mcp.json` |
| Model too large | 14B = ~13 GB. If OOM, try 8B (4.6 GB) |

---

## GitHub Repos & Downloads Master List

### Your Repos
- https://github.com/isndotbiz/mlx-models — MCP agent + configs
- https://github.com/isndotbiz/rag-system — RAG pipeline + ChromaDB

### Infrastructure
- https://github.com/vllm-project/vllm — CUDA inference server (Windows/NAS)
- https://github.com/ollama/ollama — Cross-platform inference (simpler alternative)
- https://lmstudio.ai — GUI model server (Mac/Windows)
- https://github.com/opencode-ai/opencode — Local coding assistant

### Libraries
- https://github.com/chroma-core/chroma — Vector database
- https://github.com/modelcontextprotocol/python-sdk — MCP server SDK
- https://github.com/ml-explore/mlx-lm — Apple Silicon ML inference

### Models (HuggingFace)
- https://huggingface.co/Qwen/Qwen3-14B-AWQ — 14B for CUDA (Windows/NAS)
- https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-AWQ — 30B MoE for CUDA
- https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct-AWQ — 30B Coder for CUDA
- https://huggingface.co/mlx-community — MLX format models (Mac only)
- Search "Josiefied" + "abliterated" for uncensored variants

### NVIDIA (NAS/Windows)
- https://developer.nvidia.com/cuda-downloads — CUDA Toolkit
- https://github.com/NVIDIA/nvidia-container-toolkit — Docker GPU support
