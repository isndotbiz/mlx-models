# OpenCode Quick Start Guide

**Last Updated**: February 10, 2026

---

## Start Servers

### MLX Server (Port 11434)
```bash
cd ~/workspace/llm-security-research
./start-mlx-server.sh
```

### LM Studio Server (Port 1234)
1. Open LM Studio app
2. Load a model
3. Click "Start Server"

### Verify Both Running
```bash
curl http://localhost:11434/v1/models  # MLX
curl http://localhost:1234/v1/models   # LM Studio
```

---

## OpenCode Commands

### List Available Models
```bash
opencode models mlx        # List MLX models
opencode models lmstudio   # List LM Studio models
```

### Run Queries

#### Fast (1-2 seconds)
```bash
opencode run -m "mlx/josiefied-qwen2.5-0.5b" "Your question"
```

#### Best Quality (5 seconds)
```bash
opencode run -m "lmstudio/qwen/qwen3-coder-30b" "Write code for..."
```

#### Balanced (8B model)
```bash
opencode run -m "mlx/josiefied-qwen3-8b" "Your prompt"
```

---

## Quick Reference

| Task | Provider | Model | Speed |
|------|----------|-------|-------|
| Quick answers | MLX | josiefied-qwen2.5-0.5b | 1s ⚡ |
| Code generation | LM Studio | qwen/qwen3-coder-30b | 5s |
| Security research | MLX | josiefied-qwen3-8b | 12s |
| General use | Either | 8B models | 5-12s |

---

## Configuration

File: `~/.opencode/config.json`

```json
{
  "providers": {
    "mlx": {
      "apiKey": "not-needed",
      "baseURL": "http://localhost:11434/v1"
    },
    "lmstudio": {
      "apiKey": "not-needed",
      "baseURL": "http://localhost:1234/v1"
    }
  },
  "defaultProvider": "mlx",
  "defaultModel": "josiefied-qwen3-8b"
}
```

---

## Test Both Servers

### MLX Test
```bash
curl -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"josiefied-qwen2.5-0.5b","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'
```

### LM Studio Test
```bash
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"josiefied-qwen3-8b-abliterated-v1","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'
```

---

## Troubleshooting

### MLX Server Not Running
```bash
# Check process
ps aux | grep mlx-server

# Restart
cd ~/workspace/llm-security-research
./start-mlx-server.sh
```

### LM Studio Server Not Running
1. Open LM Studio
2. Load a model
3. Click "Start Server" button

### Check OpenCode Config
```bash
cat ~/.opencode/config.json
```

---

**See OPENCODE_INTEGRATION_TEST_REPORT.md for full details**
