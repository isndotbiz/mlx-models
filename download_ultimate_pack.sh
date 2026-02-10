#!/bin/bash

# Download ULTIMATE Pack - Best of Everything
# Curated selection for M4 Pro 24GB

set -e
source .venv/bin/activate

echo "=================================================="
echo "🏆 ULTIMATE MODEL PACK FOR M4 PRO"
echo "=================================================="
echo ""
echo "Best-in-class models across all categories:"
echo ""
echo "UNCENSORED (Security Research):"
echo "  • Josiefied-Qwen3-8B-abliterated (5GB) ⭐"
echo "  • Llama-3.2-11B-Vision-abliterated (7GB) 👁️"
echo ""
echo "REASONING:"
echo "  • DeepSeek-R1-Distill-Qwen-7B (5GB) ⭐"
echo "  • DeepSeek-R1-1.5B-3bit (1GB) ⚡"
echo ""
echo "CODING:"
echo "  • Qwen3-Coder-7B-4bit (5GB) ⭐"
echo "  • deepseek-coder-1.3b (1GB) ⚡"
echo ""
echo "GENERAL:"
echo "  • Qwen3-4B-4bit (2.5GB) - Fast daily driver"
echo ""
echo "OPTIONAL POWERHOUSE:"
echo "  • DeepSeek-R1-32B-4bit (19GB) - Near GPT-4 quality"
echo ""
echo "Total: 31GB (50GB with 32B model)"
echo ""

read -p "Continue with recommended pack? (Y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    exit 0
fi

cd mlx

echo ""
echo "=================================================="
echo "UNCENSORED MODELS"
echo "=================================================="

echo ""
echo "[1/8] Josiefied-Qwen3-8B-abliterated-v1-4bit"
huggingface-cli download mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --local-dir ./Josiefied-Qwen3-8B-abliterated-v1-4bit
echo "✓ Complete"

echo ""
echo "[2/8] Llama-3.2-11B-Vision-Instruct-abliterated"
huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-abliterated-4-bit \
  --local-dir ./Llama-3.2-11B-Vision-abliterated-4bit
echo "✓ Complete"

echo ""
echo "=================================================="
echo "REASONING MODELS"
echo "=================================================="

echo ""
echo "[3/8] DeepSeek-R1-Distill-Qwen-7B"
huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-7B \
  --local-dir ./DeepSeek-R1-Distill-Qwen-7B
echo "✓ Complete"

echo ""
echo "[4/8] DeepSeek-R1-Distill-Qwen-1.5B-3bit"
huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-1.5B-3bit \
  --local-dir ./DeepSeek-R1-Distill-Qwen-1.5B-3bit
echo "✓ Complete"

echo ""
echo "=================================================="
echo "CODING MODELS"
echo "=================================================="

echo ""
echo "[5/8] Qwen3-Coder-7B-4bit"
huggingface-cli download Qwen/Qwen3-Coder-7B-4bit-MLX \
  --local-dir ./Qwen3-Coder-7B-4bit
echo "✓ Complete"

echo ""
echo "[6/8] deepseek-coder-1.3b-base"
huggingface-cli download mlx-community/deepseek-coder-1.3b-base-mlx \
  --local-dir ./deepseek-coder-1.3b-base
echo "✓ Complete"

echo ""
echo "=================================================="
echo "GENERAL PURPOSE"
echo "=================================================="

echo ""
echo "[7/8] Qwen3-4B-4bit (Daily driver)"
huggingface-cli download Qwen/Qwen3-4B-MLX-4bit \
  --local-dir ./Qwen3-4B-4bit
echo "✓ Complete"

echo ""
echo "=================================================="
echo "OPTIONAL: MAXIMUM QUALITY"
echo "=================================================="

echo ""
read -p "[8/8] Download DeepSeek-R1-32B-4bit (19GB)? Near GPT-4 quality (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading DeepSeek-R1-32B-4bit..."
    huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit \
      --local-dir ./DeepSeek-R1-Distill-Qwen-32B-4bit
    echo "✓ Complete"
else
    echo "⊘ Skipped 32B model"
fi

cd ..

echo ""
echo "=================================================="
echo "Running performance tests..."
echo "=================================================="
echo ""

# Test suite
source .venv/bin/activate

echo "Testing 1.7B model (already installed)..."
python3 -c "
from mlx_lm import load, generate
import time

model, tokenizer = load('./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit')
start = time.time()
response = generate(model, tokenizer, prompt='Test', max_tokens=50, verbose=False)
print(f'✓ 1.7B: {(50 / (time.time() - start)):.1f} t/s')
" 2>/dev/null || echo "⊘ 1.7B test skipped"

echo "Testing 8B model (new)..."
python3 -c "
from mlx_lm import load, generate
import time

model, tokenizer = load('./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit')
start = time.time()
response = generate(model, tokenizer, prompt='Test', max_tokens=50, verbose=False)
print(f'✓ 8B: {(50 / (time.time() - start)):.1f} t/s')
" 2>/dev/null || echo "⊘ 8B test skipped"

echo ""
echo "=================================================="
echo "🏆 ULTIMATE PACK INSTALLED!"
echo "=================================================="
echo ""
echo "Your complete model arsenal:"
echo ""
echo "⚡ ULTRA-FAST (100+ t/s):"
echo "  • Josiefied-Qwen3-1.7B (already had)"
echo "  • DeepSeek-R1-1.5B"
echo "  • deepseek-coder-1.3b"
echo ""
echo "🚀 FAST (50-80 t/s):"
echo "  • Qwen3-4B"
echo "  • Josiefied-Qwen3-8B ⭐"
echo "  • DeepSeek-R1-7B"
echo "  • Qwen3-Coder-7B"
echo ""
echo "💎 HIGH QUALITY (40-50 t/s):"
echo "  • Llama-3.2-11B-Vision (multimodal!)"
echo ""
if [ -d "./mlx/DeepSeek-R1-Distill-Qwen-32B-4bit" ]; then
echo "🏆 MAXIMUM (20-30 t/s):"
echo "  • DeepSeek-R1-32B (near GPT-4!)"
echo ""
fi
echo "Usage examples:"
echo "  # Quick test"
echo "  python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit"
echo ""
echo "  # Coding task"
echo "  python3 test_model.py ./mlx/Qwen3-Coder-7B-4bit"
echo ""
echo "  # Reasoning task"
echo "  python3 test_model.py ./mlx/DeepSeek-R1-Distill-Qwen-7B"
echo ""
echo "  # LM Studio (GUI)"
echo "  open '/Applications/LM Studio.app'"
echo "  Set engine: MLX (Apple Silicon GPU)"
echo ""
echo "See COMPLETE_MODEL_CATALOG.md for full model list!"
echo ""
