# Model Issues & Fixes

## Summary
Your 1.7B model is **PERFECT** (55.6 tokens/s)! 

However, the 7B and 14B models have issues. Here's how to fix them:

## Option 1: Download Fresh, Verified Models (RECOMMENDED)

Instead of trying to fix potentially corrupted models, download fresh, verified ones:

### Replace WhiteRabbitNeo 7B with Dolphin-Qwen2.5-7B
```bash
source .venv/bin/activate

# Remove problematic model
rm -rf ./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx

# Download verified Dolphin model
huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit \
  --local-dir ./mlx/Dolphin-Qwen2.5-7B-4bit

# Test it
python3 test_model.py ./mlx/Dolphin-Qwen2.5-7B-4bit
```

### Replace 14B model with verified version
```bash
source .venv/bin/activate

# Backup problematic model (don't delete yet)
mv ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit \
   ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit.backup

# Download verified 14B model
huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit \
  --local-dir ./mlx/Qwen2.5-14B-Instruct-4bit

# Test it
python3 test_model.py ./mlx/Qwen2.5-14B-Instruct-4bit
```

## Option 2: Try Fixing Current Models

The gibberish output suggests tokenizer mismatch. Try regenerating tokenizer:

```bash
source .venv/bin/activate

# Check model files
python3 << 'EOF'
from transformers import AutoTokenizer
import os

models = [
    './mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx',
    './mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit'
]

for model_path in models:
    print(f"\nChecking {model_path}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        print(f"✓ Tokenizer loaded, vocab size: {len(tokenizer)}")
        
        # Test tokenization
        test = tokenizer.encode("Hello world")
        print(f"✓ Test encoding works: {test}")
    except Exception as e:
        print(f"✗ Error: {e}")
EOF
```

## Option 3: Use Your Working Model + Download New Ones

**Since your 1.7B model works perfectly:**

1. **Keep using it** for quick testing (55.6 tokens/s is excellent!)

2. **Download these VERIFIED models** for your security research:

```bash
source .venv/bin/activate

# Download proven-working models from mlx-community
# These are pre-tested and verified

# 1. Hermes 8B (minimal guardrails)
huggingface-cli download mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit \
  --local-dir ./mlx/Hermes-3-Llama-3.1-8B-4bit

# 2. Qwen 14B (baseline for comparison)
huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit \
  --local-dir ./mlx/Qwen2.5-14B-Instruct-4bit

# 3. Dolphin 7B (highly uncensored)
huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit \
  --local-dir ./mlx/Dolphin-Qwen2.5-7B-4bit

# Test each one
./test_optimization.sh
```

## Why This Happened

Possible causes:
1. **Incomplete download**: Model files partially downloaded
2. **Tokenizer mismatch**: Tokenizer doesn't match model weights
3. **MLX version incompatibility**: Models built with different MLX version
4. **Corrupted files**: Download got corrupted

## Prevention

Always download from **mlx-community** on Hugging Face:
- These are officially converted and tested
- Guaranteed to work with current MLX version
- Pre-quantized properly

## Quick Fix Script

```bash
#!/bin/bash
# fix_models.sh

source .venv/bin/activate

echo "Downloading verified replacement models..."

echo "[1/3] Dolphin-Qwen2.5-7B-4bit (highly uncensored)..."
huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit \
  --local-dir ./mlx/Dolphin-Qwen2.5-7B-4bit

echo "[2/3] Hermes-3-Llama-3.1-8B-4bit (minimal guardrails)..."
huggingface-cli download mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit \
  --local-dir ./mlx/Hermes-3-Llama-3.1-8B-4bit

echo "[3/3] Qwen2.5-14B-Instruct-4bit (baseline)..."
huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit \
  --local-dir ./mlx/Qwen2.5-14B-Instruct-4bit

echo ""
echo "✓ Download complete! Testing..."
./test_optimization.sh
```

Save as `fix_models.sh`, then run:
```bash
chmod +x fix_models.sh
./fix_models.sh
```

## Your Current Working Setup

**For now, use your 1.7B model - it's working perfectly!**

```bash
source .venv/bin/activate
python3 -c "
from mlx_lm import load, generate
model, tokenizer = load('./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit')
response = generate(model, tokenizer, 
    prompt='Explain cross-site scripting (XSS) vulnerabilities', 
    max_tokens=200
)
print(response)
"
```

This model is:
- ✓ Fast (55.6 tokens/s)
- ✓ Uncensored/abliterated
- ✓ Perfect for rapid testing
- ✓ Only 938MB (run multiple simultaneously!)
