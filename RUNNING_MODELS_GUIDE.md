# 🚀 Complete Guide to Running MLX Models

**Platform**: M4 Pro (24GB) + MLX
**Last Updated**: February 9, 2026

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Command Line Usage](#command-line-usage)
3. [Python API](#python-api)
4. [LM Studio (GUI)](#lm-studio-gui)
5. [Advanced Options](#advanced-options)
6. [Performance Optimization](#performance-optimization)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Integration Examples](#integration-examples)

---

## 🎯 Quick Start

### Basic Command
```bash
cd /Users/jonathanmallinger/models
source .venv/bin/activate
python3 test_model.py ./mlx/MODEL_NAME
```

### Your Models (Copy-Paste Ready)
```bash
# Fastest (400+ tok/s)
python3 test_model.py ./mlx/Josiefied-Qwen2.5-0.5B-abliterated

# Best balance (117 tok/s)
python3 test_model.py ./mlx/Josiefied-Qwen2.5-3B-abliterated

# Most capable (quality over speed)
python3 test_model.py ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit

# Security specialist
python3 test_model.py ./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx
```

---

## 💻 Command Line Usage

### Method 1: mlx-lm CLI (Official)

#### Generate Text
```bash
# Basic generation
mlx_lm.generate \
  --model ./mlx/Qwen3-4B-4bit \
  --prompt "Explain SQL injection:" \
  --max-tokens 200

# Interactive mode
mlx_lm.generate \
  --model ./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit \
  --max-tokens 500

# Verbose mode (shows speed)
mlx_lm.generate \
  --model ./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit \
  --prompt "Your prompt here" \
  --verbose
```

#### With Parameters
```bash
mlx_lm.generate \
  --model ./mlx/mistral-7b \
  --prompt "Write a Python function:" \
  --max-tokens 300 \
  --temp 0.7 \
  --top-p 0.9 \
  --repetition-penalty 1.1 \
  --repetition-context-size 20
```

#### Streaming Output
```bash
# Output appears as it's generated
mlx_lm.generate \
  --model ./mlx/Qwen3-4B-4bit \
  --prompt "Your prompt" \
  --max-tokens 500 \
  --verbose
```

#### Chat Mode
```bash
# Interactive chat session
mlx_lm.generate \
  --model ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --max-tokens 500

# Then type your prompts interactively
```

### Method 2: Python One-Liners

```bash
# Quick test
python3 -c "
from mlx_lm import load, generate
model, tokenizer = load('./mlx/Qwen3-4B-4bit')
print(generate(model, tokenizer, prompt='What is XSS?', max_tokens=100))
"

# With timing
python3 -c "
import time
from mlx_lm import load, generate
model, tokenizer = load('./mlx/Josiefied-Qwen2.5-0.5B-abliterated')
start = time.time()
result = generate(model, tokenizer, prompt='Test', max_tokens=100)
print(f'Speed: {100/(time.time()-start):.1f} tok/s')
"
```

---

## 🐍 Python API

### Basic Usage

```python
from mlx_lm import load, generate

# Load model
model, tokenizer = load("./mlx/Qwen3-4B-4bit")

# Generate
response = generate(
    model,
    tokenizer,
    prompt="Explain SQL injection:",
    max_tokens=200,
    verbose=True
)

print(response)
```

### Advanced Usage

```python
#!/usr/bin/env python3
"""Advanced MLX model usage"""

from mlx_lm import load, generate
import mlx.core as mx
import time

# Load model
print("Loading model...")
model, tokenizer = load("./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit")

# Configure generation parameters
prompt = """You are a security researcher. Explain how to test for SQL injection
vulnerabilities in a web application."""

# Generate with custom parameters
response = generate(
    model,
    tokenizer,
    prompt=prompt,
    max_tokens=500,
    temp=0.7,              # Temperature (0.0-2.0, default 0.7)
    top_p=0.9,             # Nucleus sampling (0.0-1.0, default 1.0)
    repetition_penalty=1.1, # Prevent repetition (1.0 = no penalty)
    repetition_context_size=20,
    verbose=True           # Show generation speed
)

print(f"\nResponse:\n{response}")
```

### Batch Processing

```python
#!/usr/bin/env python3
"""Process multiple prompts efficiently"""

from mlx_lm import load, generate
import time

# Load model once
model, tokenizer = load("./mlx/Qwen3-4B-4bit")

# Multiple prompts
prompts = [
    "What is XSS?",
    "Explain CSRF attacks:",
    "How does SQL injection work?",
    "Describe buffer overflow vulnerabilities:",
]

results = []
total_start = time.time()

for i, prompt in enumerate(prompts, 1):
    print(f"\nProcessing {i}/{len(prompts)}...")

    start = time.time()
    response = generate(model, tokenizer, prompt=prompt, max_tokens=100, verbose=False)
    duration = time.time() - start

    results.append({
        'prompt': prompt,
        'response': response,
        'time': duration
    })

total_time = time.time() - total_start
print(f"\n✓ Processed {len(prompts)} prompts in {total_time:.2f}s")
print(f"  Average: {total_time/len(prompts):.2f}s per prompt")
```

### Memory Monitoring

```python
#!/usr/bin/env python3
"""Monitor memory usage during inference"""

from mlx_lm import load, generate
import mlx.core as mx

# Reset memory tracking
mx.metal.reset_peak_memory()

# Load model
model, tokenizer = load("./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit")
load_memory = mx.metal.get_peak_memory() / (1024**3)

print(f"Memory after load: {load_memory:.2f} GB")

# Reset for inference
mx.metal.reset_peak_memory()

# Generate
response = generate(model, tokenizer, prompt="Test", max_tokens=200)

# Check memory usage
inference_memory = mx.metal.get_peak_memory() / (1024**3)
current_memory = mx.metal.get_active_memory() / (1024**3)

print(f"Peak inference memory: {inference_memory:.2f} GB")
print(f"Current active memory: {current_memory:.2f} GB")
print(f"Total memory used: {load_memory + inference_memory:.2f} GB")
```

### Streaming Generation

```python
#!/usr/bin/env python3
"""Stream tokens as they're generated"""

from mlx_lm import load, stream_generate

model, tokenizer = load("./mlx/Qwen3-4B-4bit")

prompt = "Write a detailed explanation of SQL injection:"

print("Response: ", end="", flush=True)

# Stream tokens
for token in stream_generate(
    model,
    tokenizer,
    prompt=prompt,
    max_tokens=300
):
    print(token, end="", flush=True)

print("\n")
```

### Chat Session

```python
#!/usr/bin/env python3
"""Multi-turn chat session with context"""

from mlx_lm import load, generate

model, tokenizer = load("./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit")

conversation_history = ""

print("Chat started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ['exit', 'quit', 'q']:
        break

    # Build context-aware prompt
    full_prompt = conversation_history + f"\nUser: {user_input}\nAssistant:"

    # Generate response
    response = generate(
        model,
        tokenizer,
        prompt=full_prompt,
        max_tokens=500,
        verbose=False
    )

    print(f"Assistant: {response}\n")

    # Update history
    conversation_history = full_prompt + f" {response}"

    # Trim history if too long (keep last 2000 chars)
    if len(conversation_history) > 2000:
        conversation_history = conversation_history[-2000:]
```

---

## 🖥️ LM Studio (GUI)

### Initial Setup

1. **Run setup script** (if not done already):
```bash
./setup_lm_studio.sh
```

2. **Configure LM Studio**:
   - Open LM Studio
   - Go to **Settings → Inference**
   - Set Engine: **"MLX (Apple Silicon GPU)"** ← Critical!
   - Go to **Settings → Models**
   - Click "Add Folder"
   - Select: `/Users/jonathanmallinger/models/mlx`

### Loading Models

1. **In LM Studio**:
   - Click "Load Model" (top left)
   - Your 10 models will appear
   - Select one (e.g., "Josiefied-Qwen3-8B-abliterated-v1-4bit")
   - Click "Load"

2. **Recommended Settings**:

**For Fast Models (0.5B-4B)**:
- Context Length: 8192-16384
- Temperature: 0.7
- Top-P: 0.9
- GPU Layers: Max

**For Medium Models (7-8B)**:
- Context Length: 4096-8192
- Temperature: 0.7
- Top-P: 0.9
- GPU Layers: Max

**For Large Models (14B)**:
- Context Length: 4096
- Temperature: 0.7
- Top-P: 0.9
- GPU Layers: Max

### Chat Interface

1. Type your prompt in the chat box
2. Press Enter or click Send
3. First message will be slow (compilation)
4. Subsequent messages are much faster

### Server Mode

LM Studio can run as an OpenAI-compatible API server:

1. **In LM Studio**:
   - Click "Start Server" (top right)
   - Default port: 1234
   - Endpoint: `http://localhost:1234/v1`

2. **Test with curl**:
```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is SQL injection?"}
    ],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

3. **Use from Python**:
```python
import requests

response = requests.post(
    "http://localhost:1234/v1/chat/completions",
    json={
        "messages": [
            {"role": "user", "content": "Explain XSS attacks"}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
)

print(response.json()['choices'][0]['message']['content'])
```

---

## ⚙️ Advanced Options

### Generation Parameters

```python
response = generate(
    model,
    tokenizer,
    prompt="Your prompt",

    # Core parameters
    max_tokens=500,              # Maximum tokens to generate
    temp=0.7,                    # Temperature (0.0-2.0)
                                 # Lower = more focused, higher = more creative

    top_p=0.9,                   # Nucleus sampling (0.0-1.0)
                                 # Lower = more focused on likely tokens

    # Repetition control
    repetition_penalty=1.1,      # Penalty for repeating tokens (1.0 = none)
    repetition_context_size=20,  # How many recent tokens to check

    # Output control
    verbose=True,                # Show generation speed
)
```

### Temperature Guide

```python
# Creative writing, brainstorming
temp=1.0 to 1.5

# Balanced (default)
temp=0.7 to 0.9

# Factual, deterministic
temp=0.1 to 0.3

# Most deterministic (nearly same output every time)
temp=0.0
```

### Context Length Optimization

```python
# For fast models (0.5B-4B)
max_tokens=500    # Interactive use
max_tokens=2000   # Longer generation

# For medium models (7-8B)
max_tokens=300    # Fast response
max_tokens=1000   # Balanced

# For large models (14B)
max_tokens=200    # Fast response
max_tokens=500    # Quality generation
```

### KV Cache Control

```bash
# Limit KV cache size for memory efficiency
mlx_lm.generate \
  --model ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit \
  --max-kv-size 4096 \
  --prompt "Your prompt"

# Larger cache = better quality, more memory
# Smaller cache = less memory, may affect long contexts
```

---

## 🚀 Performance Optimization

### 1. Warm Up Models

Models are slow on first run due to compilation. Warm them up:

```python
from mlx_lm import load, generate

# Load model
model, tokenizer = load("./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit")

# Warm up (5-10 iterations)
for _ in range(10):
    _ = generate(model, tokenizer, prompt="test", max_tokens=10, verbose=False)

# Now use normally (much faster!)
response = generate(model, tokenizer, prompt="Your actual prompt", max_tokens=500)
```

### 2. Memory Management

```python
import mlx.core as mx

# Set memory limits (20GB for models, 2GB cache)
mx.metal.set_memory_limit(20 * 1024**3)
mx.metal.set_cache_limit(2 * 1024**3)

# Clear cache if needed
mx.metal.clear_cache()
```

### 3. Batch Processing Strategy

```python
# Good: Load once, process many
model, tokenizer = load("./mlx/Qwen3-4B-4bit")
for prompt in prompts:
    result = generate(model, tokenizer, prompt=prompt)

# Bad: Load for each prompt (slow!)
for prompt in prompts:
    model, tokenizer = load("./mlx/Qwen3-4B-4bit")  # Don't do this!
    result = generate(model, tokenizer, prompt=prompt)
```

### 4. Parallel Model Execution

Run multiple small models simultaneously:

```bash
# Terminal 1
python3 -c "from mlx_lm import load, generate; m,t=load('./mlx/Qwen3-4B-4bit'); print(generate(m,t,prompt='Q1'))"

# Terminal 2 (simultaneously)
python3 -c "from mlx_lm import load, generate; m,t=load('./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit'); print(generate(m,t,prompt='Q2'))"

# Both run smoothly on 24GB M4 Pro!
```

### 5. Model Selection Strategy

```python
# Decision tree for model selection
def select_model(task_complexity, speed_priority):
    if speed_priority == "critical":
        return "./mlx/Josiefied-Qwen2.5-0.5B-abliterated"  # 400+ t/s

    if task_complexity == "simple":
        return "./mlx/Qwen3-4B-4bit"  # 47 t/s, good quality

    if task_complexity == "medium":
        return "./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit"  # High quality

    if task_complexity == "complex":
        return "./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit"  # Best quality

    # Default
    return "./mlx/Josiefied-Qwen2.5-3B-abliterated"  # 117 t/s, balanced
```

---

## 🏭 Production Deployment

### Option 1: vLLM-MLX (High Throughput)

#### Installation
```bash
source .venv/bin/activate
pip install git+https://github.com/waybarrios/vllm-mlx.git
```

#### Basic Server
```bash
vllm serve ./mlx/Qwen3-4B-4bit --port 8000
```

#### Production Configuration
```bash
vllm serve ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --host 0.0.0.0 \
  --port 8000 \
  --max-num-seqs 16 \
  --max-model-len 8192 \
  --enable-prefix-caching \
  --gpu-memory-utilization 0.90
```

#### Client Usage
```python
import requests

response = requests.post(
    "http://localhost:8000/v1/completions",
    json={
        "model": "model",
        "prompt": "What is SQL injection?",
        "max_tokens": 200,
        "temperature": 0.7
    }
)

print(response.json()['choices'][0]['text'])
```

### Option 2: Flask API Wrapper

```python
#!/usr/bin/env python3
"""Simple Flask API for MLX models"""

from flask import Flask, request, jsonify
from mlx_lm import load, generate
import threading

app = Flask(__name__)

# Load model at startup
print("Loading model...")
model, tokenizer = load("./mlx/Qwen3-4B-4bit")
model_lock = threading.Lock()

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 200)
    temperature = data.get('temperature', 0.7)

    with model_lock:
        response = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=temperature,
            verbose=False
        )

    return jsonify({
        'response': response,
        'model': 'Qwen3-4B-4bit'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Run it:
```bash
python3 api_server.py

# Test
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is XSS?", "max_tokens": 100}'
```

### Option 3: FastAPI (Async)

```python
#!/usr/bin/env python3
"""FastAPI async server for MLX models"""

from fastapi import FastAPI
from pydantic import BaseModel
from mlx_lm import load, generate
import asyncio

app = FastAPI()

# Load model
model, tokenizer = load("./mlx/Josiefied-Qwen2.5-3B-abliterated")

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 200
    temperature: float = 0.7

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: generate(
            model,
            tokenizer,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temp=request.temperature,
            verbose=False
        )
    )

    return {"response": response}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

Run it:
```bash
pip install fastapi uvicorn
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 1
```

---

## 🔧 Troubleshooting

### Problem: Model loads slowly

**Solution**:
```python
# Models compile on first use. Warm up after loading:
for _ in range(5):
    generate(model, tokenizer, prompt="test", max_tokens=5, verbose=False)
```

### Problem: Out of memory

**Solutions**:
```python
# 1. Use smaller model
model = load("./mlx/Josiefied-Qwen2.5-0.5B-abliterated")

# 2. Reduce context length
response = generate(model, tokenizer, prompt="...", max_tokens=100)

# 3. Clear cache
import mlx.core as mx
mx.metal.clear_cache()

# 4. Close other applications
# 5. Use model with lower bit quantization (3-bit vs 4-bit)
```

### Problem: Slow generation speed

**Solutions**:
```python
# 1. Warm up model (compile shaders)
for _ in range(10):
    generate(model, tokenizer, prompt="test", max_tokens=10)

# 2. Use smaller context
max_tokens=100  # instead of 500

# 3. Close other GPU-using apps
# 4. Use faster model
model = load("./mlx/Josiefied-Qwen2.5-0.5B-abliterated")  # 400+ t/s
```

### Problem: Repetitive output

**Solutions**:
```python
# Increase repetition penalty
response = generate(
    model,
    tokenizer,
    prompt="...",
    repetition_penalty=1.2,  # Higher = less repetition
    repetition_context_size=50
)

# Or adjust temperature
temp=0.8  # Higher = more diverse
```

### Problem: Nonsensical output

**Solutions**:
```python
# Lower temperature
temp=0.3  # More focused, deterministic

# Adjust top_p
top_p=0.85  # More selective token sampling

# Use better prompt
prompt = "You are a security expert. Explain clearly: What is SQL injection?"
```

---

## 🔗 Integration Examples

### Jupyter Notebook

```python
# Cell 1: Setup
from mlx_lm import load, generate
import mlx.core as mx

model, tokenizer = load("./mlx/Qwen3-4B-4bit")
print("✓ Model loaded")

# Cell 2: Test
response = generate(
    model,
    tokenizer,
    prompt="What is XSS?",
    max_tokens=200
)
print(response)

# Cell 3: Monitor memory
memory = mx.metal.get_active_memory() / (1024**3)
print(f"Memory: {memory:.2f} GB")
```

### VS Code Extension

```python
# Create: ~/.vscode/mlx_helper.py
from mlx_lm import load, generate

MODEL_PATH = "/Users/jonathanmallinger/models/mlx/Qwen3-4B-4bit"
model, tokenizer = load(MODEL_PATH)

def ask(question):
    return generate(model, tokenizer, prompt=question, max_tokens=200, verbose=False)

# Use in terminal:
# python3 -c "from mlx_helper import ask; print(ask('What is SQL injection?'))"
```

### Shell Integration

Add to `~/.zshrc` or `~/.bashrc`:
```bash
# Quick MLX query function
mlx-ask() {
    cd /Users/jonathanmallinger/models
    source .venv/bin/activate
    python3 -c "
from mlx_lm import load, generate
m,t=load('./mlx/Qwen3-4B-4bit')
print(generate(m,t,prompt='$1',max_tokens=200,verbose=False))
    "
}

# Usage: mlx-ask "What is XSS?"
```

### Raycast/Alfred Script

```bash
#!/bin/bash
# Save as: mlx-query.sh

cd /Users/jonathanmallinger/models
source .venv/bin/activate

python3 << EOF
from mlx_lm import load, generate
model, tokenizer = load("./mlx/Qwen3-4B-4bit")
response = generate(model, tokenizer, prompt="${1}", max_tokens=200)
print(response)
EOF
```

---

## 📝 Quick Reference Card

### Most Common Commands

```bash
# Test model
python3 test_model.py ./mlx/MODEL_NAME

# Generate text (CLI)
mlx_lm.generate --model ./mlx/MODEL_NAME --prompt "Your prompt"

# Generate text (Python)
python3 -c "from mlx_lm import load,generate; m,t=load('./mlx/MODEL');print(generate(m,t,prompt='Q'))"

# Check memory
python3 -c "import mlx.core as mx; print(f'{mx.metal.get_active_memory()/1024**3:.2f}GB')"

# List models
ls -lh mlx/

# Start LM Studio
open "/Applications/LM Studio.app"
```

### Parameter Cheat Sheet

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `temp` | 0.0-2.0 | 0.7 | Randomness (lower=focused) |
| `top_p` | 0.0-1.0 | 1.0 | Token selection (lower=focused) |
| `max_tokens` | 1-∞ | 100 | Output length |
| `repetition_penalty` | 1.0-2.0 | 1.0 | Prevent loops (higher=more penalty) |

### Model Selection Quick Guide

| Need | Use This Model |
|------|----------------|
| Speed > Quality | Qwen 0.5B (400+ t/s) |
| Balanced | Qwen 3B (117 t/s) |
| Quality > Speed | Josiefied-14B |
| Security Work | WhiteRabbitNeo |
| Uncensored | Josiefied series |
| Different arch | Gemma 4B or mistral-7b |

---

## 🎓 Best Practices

1. **Always warm up models** - First 5-10 generations compile shaders
2. **Load once, use many** - Don't reload model for each query
3. **Monitor memory** - Use `mx.metal.get_active_memory()`
4. **Choose right model** - Don't use 14B for simple questions
5. **Adjust context** - Smaller `max_tokens` = faster generation
6. **Use streaming** - For long outputs, stream tokens
7. **Clear cache periodically** - If running many different models
8. **Close other apps** - When using large models (14B)
9. **Save responses** - Models don't remember past conversations
10. **Experiment** - Try different models for same task

---

## 📚 Additional Resources

- **MLX Documentation**: https://ml-explore.github.io/mlx/
- **MLX-LM GitHub**: https://github.com/ml-explore/mlx-lm
- **Your Model List**: `cat VERIFIED_MODELS.md`
- **Use Cases**: `cat MODEL_USE_CASES.md`
- **Quick Commands**: `cat QUICK_TEST_COMMANDS.md`

---

**You're all set!** Pick a model and start generating! 🚀
