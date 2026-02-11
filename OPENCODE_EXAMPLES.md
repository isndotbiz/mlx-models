# OpenCode with Speculative Decoding - Usage Guide

## Overview

This guide shows how to use OpenCode with three different providers:
1. **Speculative** (port 8000) - Fast inference with speculative decoding
2. **MLX** (port 11434) - Standard MLX inference
3. **LM Studio** (port 1234) - LM Studio inference

## Provider Configuration

### Speculative Provider (Fastest)
- **Port**: 8000
- **Technology**: MLX + Speculative Decoding
- **Speed**: 1.5-3x faster than standard inference
- **Model**: Qwen2.5 3B (draft) + Josiefied Qwen2.5 3B (target)
- **Best for**: Fast prototyping, quick responses

### MLX Provider
- **Port**: 11434
- **Technology**: Standard MLX inference
- **Models**: All 10 models in the mlx directory
- **Best for**: Balanced performance, reliable inference

### LM Studio Provider
- **Port**: 1234
- **Technology**: LM Studio runtime
- **Models**: All 10 models + additional LM Studio models
- **Best for**: GUI-based model management

## Available Models

### Common Models Across All Providers

| Model | Context | Output | Size | Notes |
|-------|---------|--------|------|-------|
| josiefied-qwen3-14b | 32768 | 8192 | 14B | Best overall quality |
| josiefied-qwen3-8b | 32768 | 8192 | 8B | Good balance |
| josiefied-qwen2.5-3b | 32768 | 8192 | 3B | Fast, decent quality |
| qwen3-4b | 32768 | 8192 | 4B | General purpose |
| mistral-7b | 8192 | 4096 | 7B | Code-focused |
| gemma-3-4b-abliterated | 8192 | 4096 | 4B | Uncensored |
| deepseek-r1-distill-qwen-1.5b | 32768 | 8192 | 1.5B | Reasoning model |
| josiefied-qwen3-1.7b | 32768 | 8192 | 1.7B | Small, fast |
| josiefied-qwen2.5-0.5b | 32768 | 4096 | 0.5B | Ultra-fast |

### Speculative Provider Only

| Model | Context | Output | Speed Boost | Notes |
|-------|---------|--------|-------------|-------|
| qwen2.5-3b-speculative | 32768 | 8192 | 1.5-3x | Uses draft model for speculation |

## Usage Examples

### 1. Using Speculative Decoding (Default, Fastest)

```bash
# Default model is now speculative
opencode "Write a Python function to sort a list"

# Explicitly specify speculative model
opencode --model speculative/qwen2.5-3b-speculative "Explain async/await in Python"
```

### 2. Using MLX Provider

```bash
# Use best quality model
opencode --model mlx/josiefied-qwen3-14b "Write a complex sorting algorithm"

# Use faster model
opencode --model mlx/josiefied-qwen2.5-3b "Quick code review of this file"

# Use reasoning model
opencode --model mlx/deepseek-r1-distill-qwen-1.5b "Explain the reasoning behind this algorithm"
```

### 3. Using LM Studio Provider

```bash
# Use LM Studio's interface for model management
opencode --model lmstudio/josiefied-qwen3-14b "Generate API documentation"

# Use smaller model for quick tasks
opencode --model lmstudio/josiefied-qwen2.5-0.5b "Format this JSON"
```

## Speed Comparison Commands

### Benchmark: Same Prompt, Different Providers

```bash
# Test speculative decoding (fastest)
time opencode --model speculative/qwen2.5-3b-speculative "Write a Python function to reverse a string"

# Test standard MLX inference
time opencode --model mlx/josiefied-qwen2.5-3b "Write a Python function to reverse a string"

# Test LM Studio
time opencode --model lmstudio/josiefied-qwen2.5-3b "Write a Python function to reverse a string"
```

Expected results:
- Speculative: ~1.5-3x faster than standard
- MLX: Baseline performance
- LM Studio: Similar to MLX, may vary based on settings

## System Prompt Integration

### Using Custom System Prompts

```bash
# With speculative decoding
opencode --system "You are a Python expert. Be concise." \
  --model speculative/qwen2.5-3b-speculative \
  "Explain decorators"

# With MLX
opencode --system "You are a code reviewer. Focus on security." \
  --model mlx/josiefied-qwen3-14b \
  "Review this authentication code"
```

### Recommended System Prompts by Task

#### For Code Generation (Speculative)
```bash
opencode --system "You are an expert programmer. Write clean, efficient code with comments." \
  --model speculative/qwen2.5-3b-speculative \
  "Create a REST API with FastAPI"
```

#### For Code Review (Best Model)
```bash
opencode --system "You are a senior code reviewer. Focus on: 1) Security 2) Performance 3) Maintainability" \
  --model mlx/josiefied-qwen3-14b \
  "Review this authentication system"
```

#### For Quick Explanations (Fast Model)
```bash
opencode --system "You are a technical writer. Explain concepts clearly and concisely." \
  --model mlx/josiefied-qwen2.5-3b \
  "What is async programming?"
```

#### For Reasoning Tasks (Reasoning Model)
```bash
opencode --system "Think step by step. Show your reasoning process." \
  --model mlx/deepseek-r1-distill-qwen-1.5b \
  "How would you optimize this algorithm?"
```

## Model Selection Guide

### When to Use Each Provider

**Use Speculative (Default)** when:
- You need fast responses
- Working on prototyping or iteration
- Quality requirements are moderate
- Working with code generation

**Use MLX** when:
- You need reliable, consistent performance
- Working on production code
- Quality is more important than speed
- You want specific model characteristics (reasoning, uncensored, etc.)

**Use LM Studio** when:
- You prefer GUI-based model management
- You want to use additional models from LM Studio
- You need to switch models frequently with a visual interface

### Model Size Selection

| Task Complexity | Recommended Model | Provider |
|----------------|-------------------|----------|
| Simple/Quick | josiefied-qwen2.5-0.5b | Any |
| Fast iteration | qwen2.5-3b-speculative | Speculative |
| Balanced | josiefied-qwen2.5-3b | MLX/LM Studio |
| High quality | josiefied-qwen3-14b | MLX/LM Studio |
| Reasoning | deepseek-r1-distill-qwen-1.5b | MLX/LM Studio |

## Server Management

### Starting Servers

```bash
# Start speculative server (port 8000)
# See separate server startup script

# Start MLX server (port 11434)
mlx_lm.server --model /Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-3B-abliterated

# LM Studio runs on port 1234 (manage via GUI)
```

### Testing Server Connections

```bash
# Test speculative server
curl http://localhost:8000/v1/models

# Test MLX server
curl http://localhost:11434/v1/models

# Test LM Studio
curl http://localhost:1234/v1/models
```

### Switching Default Model

Edit `/Users/jonathanmallinger/.config/opencode/opencode.json`:

```json
{
  "model": "speculative/qwen2.5-3b-speculative"  // Fast (default)
  // OR
  "model": "mlx/josiefied-qwen3-14b"  // Best quality
  // OR
  "model": "lmstudio/josiefied-qwen3-14b"  // LM Studio
}
```

## Troubleshooting

### Server Not Responding

```bash
# Check if servers are running
lsof -i :8000  # Speculative
lsof -i :11434 # MLX
lsof -i :1234  # LM Studio

# Check logs
# MLX: Check terminal where server was started
# LM Studio: Check LM Studio logs
```

### Model Not Found

```bash
# List available models for each provider
opencode models speculative
opencode models mlx
opencode models lmstudio
```

### Slow Performance

1. **Use speculative decoding** for faster inference
2. **Choose smaller model** (e.g., 3B instead of 14B)
3. **Check system resources** (RAM, GPU memory)
4. **Reduce context length** if using long prompts

## Performance Tips

1. **Use Speculative by Default**: Set it as your default model for everyday tasks
2. **Reserve Large Models**: Use 14B models only when quality really matters
3. **Batch Similar Tasks**: Keep the same model loaded to avoid switching overhead
4. **Monitor Memory**: Larger models use more VRAM
5. **Warm Up**: First inference is slower (model loading), subsequent ones are faster

## Additional Resources

- OpenCode Docs: https://opencode.ai/docs
- MLX-LM: https://github.com/ml-explore/mlx-examples
- Speculative Decoding: Research on faster inference with draft models
- LM Studio: https://lmstudio.ai

## Example Workflows

### Workflow 1: Fast Prototyping
```bash
# Use speculative for quick iterations
opencode --model speculative/qwen2.5-3b-speculative "Generate boilerplate for Express.js API"
opencode --model speculative/qwen2.5-3b-speculative "Add authentication middleware"
opencode --model speculative/qwen2.5-3b-speculative "Add error handling"
```

### Workflow 2: Production Code Review
```bash
# Use best model for quality
opencode --model mlx/josiefied-qwen3-14b \
  --system "You are a security-focused code reviewer" \
  "Review this authentication system for vulnerabilities"
```

### Workflow 3: Learning & Exploration
```bash
# Use reasoning model for explanations
opencode --model mlx/deepseek-r1-distill-qwen-1.5b \
  --system "Explain step by step" \
  "How does async/await work in JavaScript?"
```

### Workflow 4: Mixed Approach
```bash
# Fast generation with speculative
opencode --model speculative/qwen2.5-3b-speculative "Generate initial code"

# Quality review with best model
opencode --model mlx/josiefied-qwen3-14b "Review and improve this code"

# Quick fixes with speculative
opencode --model speculative/qwen2.5-3b-speculative "Fix syntax errors"
```
