# 🚀 Quick Test Commands

Fast reference for testing your verified MLX models.

---

## Prerequisites

```bash
cd /Users/jonathanmallinger/models
source .venv/bin/activate
```

---

## ⚡ Fast Models (Interactive Use)

### Fastest Overall (92 t/s)
```bash
python3 test_model.py ./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit
```
**Use for**: Quick queries, uncensored responses, security research

### Best Reasoning (84 t/s)
```bash
python3 test_model.py ./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit
```
**Use for**: Chain-of-thought reasoning, step-by-step analysis

### Best Coding (47 t/s)
```bash
python3 test_model.py ./mlx/Qwen3-4B-4bit
```
**Use for**: Code generation, development workflow

---

## 🎯 Standard Models (Balanced)

### General Purpose
```bash
python3 test_model.py ./mlx/mistral-7b
```
**Use for**: Instruction following, general tasks

### Creative & Uncensored
```bash
python3 test_model.py ./mlx/dolphin3-8b
```
**Use for**: Creative writing, unrestricted responses

### Multilingual
```bash
python3 test_model.py ./mlx/qwen3-7b
```
**Use for**: English + Chinese, bilingual code

---

## 🎓 Specialized Models

### Security Specialist
```bash
python3 test_model.py ./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx
```
**Use for**: Pentesting, CTF, vulnerability analysis, security code review

### Uncensored 8B (High Quality)
```bash
python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit
```
**Use for**: Complex uncensored tasks, security research, quality over speed

### Most Capable (14B)
```bash
python3 test_model.py ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit
```
**Use for**: Hardest problems, best quality, when speed doesn't matter

**Note**: Close other apps before using 14B model for best performance.

---

## 🔧 Testing Workflows

### Test All Models Quickly
```bash
# Run verification script
python3 verify_all_models.py
```

### Warm Up a Model (Improve Speed)
```bash
# First generation is slow (compilation)
echo "Say hello in one word" | python3 test_model.py ./mlx/MODEL_NAME

# Now use normally - much faster!
```

### Compare Model Performance
```bash
# Test multiple models on same prompt
for model in DeepSeek-R1-Distill-Qwen-1.5B-3bit Qwen3-4B-4bit mistral-7b; do
    echo "Testing $model..."
    python3 test_model.py ./mlx/$model
done
```

---

## 🎯 Use Case Shortcuts

### Security Research Session
```bash
# Quick exploration
python3 test_model.py ./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit

# Deep analysis
python3 test_model.py ./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx
```

### Development Workflow
```bash
# Keep this running in a terminal
python3 test_model.py ./mlx/Qwen3-4B-4bit
# Fast responses for coding questions
```

### Complex Problem Solving
```bash
# Start with reasoning model
python3 test_model.py ./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit

# Escalate if needed
python3 test_model.py ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit
```

---

## 📊 Performance Comparison

| Command | Speed | Quality | Memory | Use Case |
|---------|-------|---------|--------|----------|
| `Josiefied-1.7B` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | 0.9GB | Fast queries |
| `DeepSeek-R1-1.5B` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 0.7GB | Fast reasoning |
| `Qwen3-4B` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 2.0GB | Coding |
| `mistral-7b` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 3.8GB | General use |
| `WhiteRabbitNeo` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 4.0GB | Security |
| `Josiefied-8B` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 4.3GB | Quality |
| `Josiefied-14B` | ⚡ | ⭐⭐⭐⭐⭐ | 14GB | Best quality |

---

## 💡 Pro Tips

**First Run Is Slow**:
- Models compile on first use (MLX optimization)
- Send a quick test prompt to "warm up"
- Subsequent generations are much faster

**Memory Management**:
- Can run 2-3 small models (1-4B) simultaneously
- Run 1-2 medium models (7-8B) at a time
- Dedicate system to large model (14B)

**Context Length**:
- Smaller context = faster generation
- Use 4K-8K for interactive work
- Use 16K+ only when needed

**Model Selection**:
- Start small (fast iteration)
- Escalate to larger models if quality insufficient
- Don't use 14B for simple questions

---

## 🔍 Verification

Check which models are working:
```bash
cat model_verification_results.json
```

View detailed model info:
```bash
cat VERIFIED_MODELS.md
```

View use case guide:
```bash
cat MODEL_USE_CASES.md
```

---

## 🚀 LM Studio Integration

Run the setup script:
```bash
./setup_lm_studio.sh
```

Then in LM Studio:
1. Settings → Inference → Engine → **MLX**
2. Settings → Models → Add Path → `/Users/jonathanmallinger/models/mlx`
3. Load any model and start chatting!

---

**Quick Start**: Copy-paste any command above to test that specific model immediately!
