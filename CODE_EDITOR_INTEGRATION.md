# 💻 Code Editor Integration - MLX Models

Connect your local MLX models to VS Code, Cursor, and other code editors.

---

## 🚀 Option 1: Continue.dev (Recommended for Coding)

### Installation

```bash
# Install Continue extension in VS Code/Cursor
# 1. Open VS Code/Cursor
# 2. Extensions → Search "Continue"
# 3. Install "Continue - Codestral, Claude, and more"
```

### Configuration

Create/edit `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Josiefied 8B (Local - Champion)",
      "provider": "openai",
      "model": "model",
      "apiBase": "http://localhost:8000/v1",
      "apiKey": "not-needed",
      "description": "Local MLX - Security research champion (44% jailbreak success)"
    },
    {
      "title": "Qwen 0.5B (Local - Ultra Fast)",
      "provider": "openai",
      "model": "model",
      "apiBase": "http://localhost:11434/v1",
      "apiKey": "not-needed",
      "description": "Local MLX - Fastest model (235 tok/s)"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Local Fast Model",
    "provider": "openai",
    "model": "model",
    "apiBase": "http://localhost:8000/v1",
    "apiKey": "not-needed"
  },
  "embeddingsProvider": {
    "provider": "openai",
    "model": "text-embedding-ada-002",
    "apiBase": "http://localhost:8000/v1",
    "apiKey": "not-needed"
  }
}
```

**Usage in VS Code/Cursor**:
- `Cmd+L` - Open chat with your local model
- `Cmd+I` - Inline code editing
- Tab - Autocomplete with local model

---

## 🎯 Option 2: GitHub Copilot Alternative (Custom)

### VS Code settings.json

Add to `.vscode/settings.json`:

```json
{
  "continue.telemetryEnabled": false,
  "continue.enableTabAutocomplete": true,
  "continue.models": [
    {
      "title": "Local MLX - Josiefied 8B",
      "provider": "openai",
      "model": "model",
      "apiBase": "http://localhost:8000/v1"
    }
  ]
}
```

---

## 🔧 Option 3: Cursor IDE Integration

### Cursor Settings

1. Open Cursor
2. Settings → Models → Add Custom Model
3. Configure:
   - **Provider**: OpenAI Compatible
   - **Base URL**: http://localhost:8000/v1
   - **API Key**: (leave empty or use "not-needed")
   - **Model**: model

**Features**:
- `Cmd+K` - AI chat in Cursor
- `Cmd+L` - Composer mode
- Tab autocomplete

---

## 🎨 Option 4: Cline (Claude Code Alternative)

### Installation

```bash
# Install Cline extension in VS Code
# Extensions → Search "Cline"
```

### Configuration

Settings → Cline → API Configuration:

```
Provider: OpenAI Compatible
Base URL: http://localhost:8000/v1
API Key: not-needed
Model: model
```

**Usage**:
- Open Cline panel
- Chat with your local Josiefied 8B
- No API costs!
- 100% private

---

## 🚀 Option 5: REST Client (Simple Testing)

### VS Code REST Client

Install "REST Client" extension, then create `test-api.http`:

```http
### Test 1: List models
GET http://localhost:8000/v1/models

### Test 2: Chat completion
POST http://localhost:8000/v1/chat/completions
Content-Type: application/json

{
  "model": "model",
  "messages": [
    {"role": "user", "content": "Explain SQL injection"}
  ],
  "max_tokens": 200
}

### Test 3: Code generation
POST http://localhost:8000/v1/completions
Content-Type: application/json

{
  "model": "model",
  "prompt": "Write a Python function to validate email:",
  "max_tokens": 150
}
```

Click "Send Request" above each request to test!

---

## 💡 Switching Between Models

### For Different Tasks

**Fast autocomplete** (port 11434):
```json
{
  "apiBase": "http://localhost:11434/v1",
  "model": "model"
}
```

**Quality code review** (port 8000):
```json
{
  "apiBase": "http://localhost:8000/v1",
  "model": "model"
}
```

### Start Different Model on Port

```bash
# Stop current
kill $(cat vllm-server.pid)

# Start fast model for autocomplete
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen2.5-0.5B-abliterated --port 8000 &

# Or start quality model
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --port 8000 &
```

---

## 🎯 Recommended Setup

**For Coding Assistance:**

1. **Port 8000**: Josiefied 8B (quality responses)
2. **Port 11434**: Already running (check what model)
3. **Configure Continue.dev** to use both

**Workflow**:
- Fast completions → Port 11434
- Code explanations → Port 8000 (Josiefied 8B)
- Security code review → Port 8000

---

## 📊 Performance by Task

| Task | Best Model | Port | Speed | Quality |
|------|------------|------|-------|---------|
| Autocomplete | Qwen 0.5B | 11434* | 235 t/s | ⭐⭐⭐ |
| Code review | Josiefied 8B | 8000 | 40 t/s | ⭐⭐⭐⭐⭐ |
| Explanations | Qwen 3B | - | 90 t/s | ⭐⭐⭐⭐ |
| Refactoring | Josiefied 8B | 8000 | 40 t/s | ⭐⭐⭐⭐⭐ |
| Security analysis | Josiefied 8B | 8000 | 40 t/s | ⭐⭐⭐⭐⭐ |

*Check what's running on 11434

---

## ✅ Quick Setup Commands

### For VS Code/Cursor with Continue.dev:

```bash
# Create config
mkdir -p ~/.continue
cat > ~/.continue/config.json << 'EOF'
{
  "models": [
    {
      "title": "Local Josiefied 8B",
      "provider": "openai",
      "model": "model",
      "apiBase": "http://localhost:8000/v1",
      "apiKey": "not-needed"
    }
  ]
}
EOF

# Install Continue extension
# Then restart VS Code/Cursor
```

### Test in Terminal:

```bash
# Test code generation
curl -X POST http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "prompt": "def validate_email(email):\n    # Check if email is valid\n",
    "max_tokens": 100
  }'
```

---

**Want me to check what's running on port 11434 and create the Continue.dev config?**
