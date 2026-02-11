# LM Studio CLI Quick Start Guide with Extensions

**Platform**: M4 Pro (24GB) + MLX
**Last Updated**: February 10, 2026
**LM Studio Version**: 0.4.0+

---

## Table of Contents

1. [Starting the Server](#1-starting-the-server)
2. [Extension Benefits](#2-extension-benefits)
3. [OpenCode Integration](#3-opencode-integration)
4. [Model Management](#4-model-management)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Starting the Server

### Basic Server Commands

#### Start the LM Studio Server
```bash
# Start the server (default port 1234)
~/.lmstudio/bin/lms server start

# Check server status
~/.lmstudio/bin/lms server status

# Stop the server
~/.lmstudio/bin/lms server stop
```

#### Load a Model Before Starting
```bash
# Load specific model
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit

# Load with custom context length
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit --context-length 8192

# Load with GPU offload control
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --gpu max

# Load with TTL (auto-unload after 1 hour of inactivity)
~/.lmstudio/bin/lms load mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit --ttl 3600
```

#### Port Configuration

**Default Port**: 1234

**Change Port** (if needed):
```bash
# Edit LM Studio settings or use environment variable
export LMS_PORT=8080
~/.lmstudio/bin/lms server start
```

**Multiple Servers** (Advanced):
```bash
# Server 1: Fast model on port 1234 (default)
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen2.5-0.5B-abliterated
~/.lmstudio/bin/lms server start

# Server 2: Quality model on different port (requires LM Studio GUI)
# Open LM Studio → Start Server → Configure port manually
```

#### Advanced Load Options

```bash
# Load for parallel requests (multiple concurrent chats)
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit --parallel 4

# Estimate resources before loading
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-14B-abliterated-v3 --estimate-only

# Load with custom identifier (for API)
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --identifier "security-model"

# Auto-approve prompts (scripting)
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit -y
```

### Complete Startup Script

Create `/Users/jonathanmallinger/models/start_lm_studio_server.sh`:

```bash
#!/bin/bash
# LM Studio Server Startup Script

set -e

MODEL_PATH="mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit"
CONTEXT_LENGTH=8192
PORT=1234

echo "Starting LM Studio Server..."
echo "Model: $MODEL_PATH"
echo "Context: $CONTEXT_LENGTH tokens"
echo "Port: $PORT"

# Load model
~/.lmstudio/bin/lms load "$MODEL_PATH" \
  --context-length $CONTEXT_LENGTH \
  --gpu max \
  --parallel 2 \
  -y

# Start server
~/.lmstudio/bin/lms server start

echo ""
echo "Server running at http://localhost:$PORT"
echo ""
echo "Test with:"
echo "curl http://localhost:$PORT/v1/models"
```

Make it executable:
```bash
chmod +x /Users/jonathanmallinger/models/start_lm_studio_server.sh
./start_lm_studio_server.sh
```

---

## 2. Extension Benefits

### MLX Runtime vs llama.cpp Performance

**Critical Performance Difference on M4 Pro:**

| Runtime | Format | Speed | Memory | Best For |
|---------|--------|-------|--------|----------|
| **MLX** | MLX | **60% faster** | Optimized | Apple Silicon (M-series) |
| llama.cpp | GGUF | Baseline | Standard | Cross-platform |

**Benchmark Results (M4 Pro, Qwen3-8B-4bit):**
- MLX: **83 tokens/s** generation
- llama.cpp: **52 tokens/s** generation
- **Performance gain: +60%**

#### Check and Select Runtime

```bash
# List installed runtimes
~/.lmstudio/bin/lms runtime ls

# Expected output:
# LLM ENGINE                                       SELECTED    MODEL FORMAT
# llama.cpp-mac-arm64-apple-metal-advsimd@2.2.0       ✓        GGUF
# mlx-llm-mac-arm64-apple-metal-advsimd@1.0.0         ✓        MLX

# Select MLX runtime (if not already selected)
~/.lmstudio/bin/lms runtime select mlx-llm-mac-arm64-apple-metal-advsimd@1.0.0
```

**Important**: Your models in `/Users/jonathanmallinger/models/mlx/` are already in MLX format and will automatically use the MLX runtime when loaded.

#### Update Runtimes

```bash
# Update all runtimes to latest versions
~/.lmstudio/bin/lms runtime update

# Survey available hardware
~/.lmstudio/bin/lms runtime survey
```

### Available Plugins

#### 1. RAG v1 (Retrieval Augmented Generation)

**Location**: `~/.lmstudio/hub/rag-v1`

**Features**:
- Upload documents for context
- Query documents with AI
- Embed and search local knowledge base

**Enable in LM Studio**:
1. Open LM Studio
2. Extensions tab → RAG v1 → Enable
3. Upload documents (PDFs, text files)
4. Chat with document context

**Develop the Plugin**:
```bash
# Navigate to plugin directory
cd ~/.lmstudio/hub/rag-v1

# Start dev server (hot reload)
~/.lmstudio/bin/lms dev

# Edit source in src/ directory
# Changes reflect immediately in LM Studio
```

#### 2. Installing More Extensions

**Browse Available Extensions**:
```bash
# List available extensions on LM Studio Hub
~/.lmstudio/bin/lms get

# Clone an extension
~/.lmstudio/bin/lms clone lmstudio/EXTENSION_NAME

# Example: Install hypothetical web search plugin
~/.lmstudio/bin/lms clone lmstudio/web-search
```

**Current Installed**:
```bash
# List installed hub artifacts
ls -la ~/.lmstudio/hub/

# Current plugins:
# - rag-v1 (Retrieval Augmented Generation)
# - models (Model presets)
# - presets (Chat presets)
```

#### 3. Publishing Your Own Plugin

```bash
# Navigate to your plugin directory
cd ~/.lmstudio/hub/my-plugin

# Login to LM Studio (first time only)
~/.lmstudio/bin/lms login

# Push to hub
~/.lmstudio/bin/lms push

# Update existing plugin
~/.lmstudio/bin/lms push
```

### Continuous Batching (MLX 1.0.0+)

**Feature**: Process multiple requests simultaneously
**Benefit**: Significant throughput improvements

**Enabled by default** when using:
- MLX runtime 1.0.0+
- `--parallel` flag with model load

```bash
# Enable continuous batching with 4 parallel slots
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit --parallel 4
```

**Use Cases**:
- Running API server with multiple clients
- Multiple concurrent chats
- Batch processing scripts

---

## 3. OpenCode Integration

### Configuration File Format

**Create** `~/.opencode/config.json` or `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "LM Studio - Josiefied 8B (Security Champion)",
      "provider": "openai",
      "model": "josiefied-qwen3-8b-abliterated-v1",
      "apiBase": "http://localhost:1234/v1",
      "apiKey": "not-needed",
      "description": "Local MLX - Security research specialist (44% jailbreak success)"
    },
    {
      "title": "LM Studio - Qwen 4B (Fast Coding)",
      "provider": "openai",
      "model": "qwen3-4b",
      "apiBase": "http://localhost:1234/v1",
      "apiKey": "not-needed",
      "description": "Local MLX - Fast coding assistant (47 tok/s)"
    },
    {
      "title": "LM Studio - DeepSeek 1.5B (Ultra Fast)",
      "provider": "openai",
      "model": "deepseek-r1-distill-qwen-1.5b",
      "apiBase": "http://localhost:1234/v1",
      "apiKey": "not-needed",
      "description": "Local MLX - Ultra fast for simple tasks (84 tok/s)"
    }
  ],
  "tabAutocompleteModel": {
    "title": "LM Studio Fast Autocomplete",
    "provider": "openai",
    "model": "deepseek-r1-distill-qwen-1.5b",
    "apiBase": "http://localhost:1234/v1",
    "apiKey": "not-needed"
  },
  "embeddingsProvider": {
    "provider": "openai",
    "model": "text-embedding-nomic-embed-text-v1.5",
    "apiBase": "http://localhost:1234/v1",
    "apiKey": "not-needed"
  }
}
```

### Switch Between Providers

#### Continue.dev / OpenCode

**Method 1: In-Editor Dropdown**
1. Open Continue panel in VS Code
2. Click model dropdown at top
3. Select from configured models
4. Start chatting

**Method 2: Keyboard Shortcut**
- `Cmd+L` - Open chat (then select model)
- `Cmd+I` - Inline edit with current model

#### Cursor IDE

**Switch Models**:
1. Open Cursor
2. Click model name at bottom
3. Select from list
4. Or: Settings → Models → Switch

#### Example Commands

**VS Code with Continue.dev**:
```bash
# Create Continue config with LM Studio
mkdir -p ~/.continue
cat > ~/.continue/config.json << 'EOF'
{
  "models": [
    {
      "title": "Local Josiefied 8B",
      "provider": "openai",
      "model": "model",
      "apiBase": "http://localhost:1234/v1",
      "apiKey": "not-needed"
    }
  ]
}
EOF

# Restart VS Code
# Press Cmd+L to open Continue
# Type your prompt
```

**Test from Terminal**:
```bash
# Test the OpenAI-compatible API
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "messages": [
      {"role": "user", "content": "Explain SQL injection"}
    ],
    "max_tokens": 200,
    "temperature": 0.7
  }'
```

**Python Script**:
```python
#!/usr/bin/env python3
"""Use LM Studio with OpenAI API format"""

import openai

# Configure OpenAI client for LM Studio
openai.api_key = "not-needed"
openai.api_base = "http://localhost:1234/v1"

response = openai.ChatCompletion.create(
    model="model",
    messages=[
        {"role": "user", "content": "What is XSS?"}
    ],
    max_tokens=200,
    temperature=0.7
)

print(response.choices[0].message.content)
```

### Multi-Model Workflow

**Use Different Models for Different Tasks**:

```bash
# Terminal 1: Load fast model for autocomplete
~/.lmstudio/bin/lms load mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit
~/.lmstudio/bin/lms server start

# Configure Continue for autocomplete on port 1234
```

```bash
# Terminal 2: Use MLX directly for quality work
cd /Users/jonathanmallinger/models
source .venv/bin/activate
python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit
```

---

## 4. Model Management

### List Available Models

```bash
# List all downloaded models
~/.lmstudio/bin/lms ls

# Expected output:
# You have 10 models, taking up 30.30 GB of disk space.
#
# LLM                                    PARAMS    ARCH       SIZE
# deepseek-r1-distill-qwen-1.5b          1.5B      Qwen2      789.27 MB
# gemma-3-4b-abliterated                 4B        gemma3     2.60 GB
# josiefied-qwen2.5-0.5b-abliterated     0.5B      Qwen2      293.99 MB
# ...
```

**List Currently Loaded Models**:
```bash
~/.lmstudio/bin/lms ps

# Shows models currently in memory with:
# - Model name
# - Context length
# - GPU offload
# - Memory usage
```

### Import Models with Symlinks

Your models are already accessible! They're in `/Users/jonathanmallinger/models/mlx/`.

**If you need to import additional models**:

```bash
# Import a model from custom location
~/.lmstudio/bin/lms import /path/to/model

# Import with automatic detection
~/.lmstudio/bin/lms import /Users/jonathanmallinger/models/mlx/NEW_MODEL

# The model will appear in 'lms ls' output
```

**Manual Symlink Method** (if needed):
```bash
# Link model directory to LM Studio models folder
ln -s /Users/jonathanmallinger/models/mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit \
      ~/.lmstudio/models/josiefied-qwen3-8b-abliterated-v1

# Verify
~/.lmstudio/bin/lms ls | grep josiefied
```

### Load/Unload Models

#### Load Models

```bash
# Interactive mode (select from list)
~/.lmstudio/bin/lms load

# Specify model directly
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit

# Load with options
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --context-length 8192 \
  --gpu max \
  --parallel 2
```

#### Unload Models

```bash
# Unload specific model
~/.lmstudio/bin/lms unload mlx/Qwen3-4B-4bit

# Unload by identifier (if set during load)
~/.lmstudio/bin/lms unload --identifier "security-model"

# Check what's loaded before unloading
~/.lmstudio/bin/lms ps
```

#### Auto-Unload with TTL

```bash
# Model auto-unloads after 30 minutes of inactivity
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --ttl 1800

# Model auto-unloads after 1 hour
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit --ttl 3600
```

### Download New Models

```bash
# Search for models
~/.lmstudio/bin/lms get "qwen"

# Interactive search and download
~/.lmstudio/bin/lms get

# The model will download to ~/.lmstudio/models/
```

**Download MLX Models from Hugging Face** (Alternative):
```bash
cd /Users/jonathanmallinger/models/mlx
source ../.venv/bin/activate

# Download MLX-formatted model
huggingface-cli download mlx-community/MODEL_NAME --local-dir ./MODEL_NAME

# Example: Download Llama 3.3 70B (large!)
huggingface-cli download mlx-community/Llama-3.3-70B-Instruct-4bit \
  --local-dir ./Llama-3.3-70B-Instruct-4bit
```

### Model Selection Quick Reference

| Task | Best Model | Size | Speed |
|------|-----------|------|-------|
| Fast autocomplete | deepseek-r1-distill-qwen-1.5b | 789 MB | 84 t/s |
| Quick questions | josiefied-qwen2.5-0.5b-abliterated | 294 MB | 400+ t/s |
| Coding | qwen3-4b | 2.15 GB | 47 t/s |
| Balanced quality | josiefied-qwen2.5-3b-abliterated | 1.75 GB | 117 t/s |
| Security work | josiefied-qwen3-8b-abliterated-v1 | 4.62 GB | 40 t/s |
| Best quality | josiefied-qwen3-14b-abliterated-v3 | 12.94 GB | 20 t/s |

---

## 5. Troubleshooting

### Common Errors and Fixes

#### Error: "Server failed to start"

**Fix 1: Check if already running**
```bash
~/.lmstudio/bin/lms server status

# If running, stop first
~/.lmstudio/bin/lms server stop

# Then start
~/.lmstudio/bin/lms server start
```

**Fix 2: Check port availability**
```bash
# Check if port 1234 is in use
lsof -i :1234

# Kill process if needed
kill -9 PID

# Or use different port
export LMS_PORT=8080
~/.lmstudio/bin/lms server start
```

**Fix 3: Check logs**
```bash
# View server logs
ls -la ~/.lmstudio/server-logs/

# Tail latest log
tail -f ~/.lmstudio/server-logs/$(ls -t ~/.lmstudio/server-logs/ | head -1)
```

#### Error: "Model not found"

**Fix 1: Verify model exists**
```bash
# List all models
~/.lmstudio/bin/lms ls

# Check model directory
ls -la /Users/jonathanmallinger/models/mlx/
```

**Fix 2: Use exact model name**
```bash
# Get exact name from ls output
~/.lmstudio/bin/lms ls | grep josiefied

# Use exact name (case-sensitive)
~/.lmstudio/bin/lms load josiefied-qwen3-8b-abliterated-v1
```

**Fix 3: Import model**
```bash
# If model not showing up, import it
~/.lmstudio/bin/lms import /Users/jonathanmallinger/models/mlx/MODEL_NAME
```

#### Error: "Out of memory" / Model load fails

**Fix 1: Unload other models**
```bash
# Check what's loaded
~/.lmstudio/bin/lms ps

# Unload models
~/.lmstudio/bin/lms unload MODEL_NAME
```

**Fix 2: Reduce context length**
```bash
# Load with smaller context
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-14B-abliterated-v3 --context-length 4096

# Instead of default (often 8192+)
```

**Fix 3: Use smaller model**
```bash
# Instead of 14B model, use 8B
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit

# Or even smaller
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit
```

**Fix 4: Close other applications**
```bash
# Check memory usage
top -o MEM

# Close memory-intensive apps (Chrome, etc.)
# Then retry
```

#### Error: "Slow inference speed"

**Fix 1: Verify MLX runtime is selected**
```bash
# Check runtime
~/.lmstudio/bin/lms runtime ls

# Should show MLX with checkmark:
# mlx-llm-mac-arm64-apple-metal-advsimd@1.0.0    ✓    MLX

# If not, select it
~/.lmstudio/bin/lms runtime select mlx-llm-mac-arm64-apple-metal-advsimd@1.0.0
```

**Fix 2: Check model is MLX format**
```bash
# Your models in mlx/ directory are already MLX format
~/.lmstudio/bin/lms ls

# Look for "MLX" in ARCH column
# If GGUF, you're using llama.cpp (slower)
```

**Fix 3: Increase GPU offload**
```bash
# Load with max GPU offload
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit --gpu max
```

**Fix 4: Reduce context length**
```bash
# Smaller context = faster generation
~/.lmstudio/bin/lms load mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --context-length 4096
```

#### Error: "Connection refused" when testing API

**Fix 1: Ensure server is running**
```bash
~/.lmstudio/bin/lms server status

# If not running
~/.lmstudio/bin/lms server start
```

**Fix 2: Check correct port**
```bash
# Default is 1234
curl http://localhost:1234/v1/models

# If using custom port
curl http://localhost:8080/v1/models
```

**Fix 3: Load a model first**
```bash
# Server needs a model loaded
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit

# Then test
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"model","messages":[{"role":"user","content":"test"}]}'
```

### Check Server Status

**Quick Status Check**:
```bash
# Check if server is running
~/.lmstudio/bin/lms server status

# Check loaded models
~/.lmstudio/bin/lms ps

# Test API endpoint
curl http://localhost:1234/v1/models
```

**Detailed Health Check**:
```bash
# Check all components
~/.lmstudio/bin/lms server status
~/.lmstudio/bin/lms ps
~/.lmstudio/bin/lms runtime ls

# Test API
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
  }'
```

### Logs Location

**Server Logs**:
```bash
# List all logs
ls -la ~/.lmstudio/server-logs/

# View latest log
tail -f ~/.lmstudio/server-logs/$(ls -t ~/.lmstudio/server-logs/ | head -1)

# Search for errors
grep -i error ~/.lmstudio/server-logs/*
```

**Application Logs**:
```bash
# LM Studio app logs
ls -la ~/.lmstudio/.internal/logs/

# View recent logs
tail -f ~/.lmstudio/.internal/logs/main.log
```

**Model Loading Logs**:
```bash
# When loading model, use verbose output
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit -y

# Watch for:
# - Loading progress
# - Memory allocation
# - GPU offload ratio
# - Context length
```

### Performance Monitoring

```bash
# Monitor memory usage
watch -n 1 'ps aux | grep -E "(lms|LM Studio)" | grep -v grep'

# Monitor GPU usage (requires sudo)
sudo powermetrics --samplers gpu_power -i 1000 -n 10

# Check LM Studio process
top -pid $(pgrep -f "LM Studio")
```

### Reset/Clean Install

**If all else fails**:

```bash
# Backup your models first!
# Models are in: /Users/jonathanmallinger/models/mlx/

# Stop server
~/.lmstudio/bin/lms server stop

# Remove LM Studio data (keeps app)
# WARNING: This removes settings and downloaded models
# mv ~/.lmstudio ~/.lmstudio.backup

# Reinstall LM Studio
# Download from: https://lmstudio.ai

# Bootstrap CLI again
~/.lmstudio/bin/lms bootstrap

# Re-import your models
~/.lmstudio/bin/lms import /Users/jonathanmallinger/models/mlx/MODEL_NAME
```

---

## Quick Reference Card

### Essential Commands

```bash
# List models
~/.lmstudio/bin/lms ls

# Load model
~/.lmstudio/bin/lms load mlx/MODEL_NAME

# Check what's loaded
~/.lmstudio/bin/lms ps

# Start server
~/.lmstudio/bin/lms server start

# Check server status
~/.lmstudio/bin/lms server status

# Stop server
~/.lmstudio/bin/lms server stop

# Unload model
~/.lmstudio/bin/lms unload MODEL_NAME

# View logs
tail -f ~/.lmstudio/server-logs/$(ls -t ~/.lmstudio/server-logs/ | head -1)
```

### Test API

```bash
# List available models
curl http://localhost:1234/v1/models

# Chat completion
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

### Your Available Models

```
Fast (0.5-1.7B): 84-400 tok/s
├── deepseek-r1-distill-qwen-1.5b (789 MB)
├── josiefied-qwen2.5-0.5b-abliterated (294 MB)
└── josiefied-qwen3-1.7b-abliterated-v1 (984 MB)

Balanced (3-4B): 47-117 tok/s
├── josiefied-qwen2.5-3b-abliterated (1.75 GB)
├── qwen3-4b (2.15 GB)
└── gemma-3-4b-abliterated (2.60 GB)

Quality (7-14B): 20-40 tok/s
├── mistral-7b (4.08 GB)
├── josiefied-qwen3-8b-abliterated-v1 (4.62 GB)
└── josiefied-qwen3-14b-abliterated-v3 (12.94 GB)

Specialized
└── text-embedding-nomic-embed-text-v1.5 (84 MB)
```

---

## Best Practices

1. **Always use MLX runtime** for Apple Silicon (60% faster than llama.cpp)
2. **Load models with appropriate context** (4096-8192 for most tasks)
3. **Use TTL for production** to auto-unload inactive models
4. **Enable parallel requests** for API server (`--parallel 2-4`)
5. **Monitor memory usage** when running large models
6. **Start with small models** for testing, scale up for quality
7. **Check server logs** when troubleshooting
8. **Use model identifiers** when running multiple models

---

## Resources

- **LM Studio Website**: https://lmstudio.ai
- **Documentation**: https://lmstudio.ai/docs
- **Discord**: https://discord.gg/lmstudio
- **Your Models**: `/Users/jonathanmallinger/models/mlx/`
- **Model Details**: `/Users/jonathanmallinger/models/VERIFIED_MODELS.md`
- **Use Cases**: `/Users/jonathanmallinger/models/MODEL_USE_CASES.md`

---

**You're all set!** Start the server, load a model, and start chatting!

```bash
# Quick start (copy-paste):
~/.lmstudio/bin/lms load mlx/Qwen3-4B-4bit --gpu max -y
~/.lmstudio/bin/lms server start
curl http://localhost:1234/v1/models
```
