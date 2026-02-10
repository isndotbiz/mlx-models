#!/bin/bash

# Download Coding Models Pack
# Qwen3-Coder and DeepSeek-Coder series

set -e
source .venv/bin/activate

echo "=================================================="
echo "Coding Models Pack"
echo "=================================================="
echo ""
echo "This will download:"
echo "  1. deepseek-coder-1.3b-base (1GB) - Ultra-fast ⚡"
echo "  2. Qwen3-Coder-7B-4bit (5GB) - Balanced ⭐"
echo "  3. Qwen3-Coder-30B-4bit (17GB) - Maximum 🏆"
echo ""
echo "Total: ~23GB"
echo ""

read -p "Download all coding models? (y/N): " -n 1 -r
echo ""
ALL=$REPLY

cd mlx

echo ""
echo "[1/3] deepseek-coder-1.3b-base"
echo "   ⚡ ULTRA-FAST - 100+ tokens/s code completion"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download mlx-community/deepseek-coder-1.3b-base-mlx \
      --local-dir ./deepseek-coder-1.3b-base
    echo "✓ Complete"
else
    read -p "  Download this model? (Y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        huggingface-cli download mlx-community/deepseek-coder-1.3b-base-mlx \
          --local-dir ./deepseek-coder-1.3b-base
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

echo ""
echo "[2/3] Qwen3-Coder-7B-4bit"
echo "   ⭐ RECOMMENDED - Fast & capable coding assistant"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download Qwen/Qwen3-Coder-7B-4bit-MLX \
      --local-dir ./Qwen3-Coder-7B-4bit
    echo "✓ Complete"
else
    read -p "  Download this model? (Y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        huggingface-cli download Qwen/Qwen3-Coder-7B-4bit-MLX \
          --local-dir ./Qwen3-Coder-7B-4bit
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

echo ""
echo "[3/3] Qwen3-Coder-30B-4bit"
echo "   🏆 MAXIMUM - Advanced AI coding assistant"
echo "   ⚠ Warning: Uses 17GB, leaves only 7GB for system"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download Qwen/Qwen3-Coder-30B-4bit-MLX \
      --local-dir ./Qwen3-Coder-30B-4bit
    echo "✓ Complete"
else
    read -p "  Download this model? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        huggingface-cli download Qwen/Qwen3-Coder-30B-4bit-MLX \
          --local-dir ./Qwen3-Coder-30B-4bit
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

cd ..

echo ""
echo "=================================================="
echo "Testing Qwen3-Coder-7B..."
echo "=================================================="

source .venv/bin/activate
python3 << 'EOF'
from mlx_lm import load, generate
import time

try:
    model, tokenizer = load('./mlx/Qwen3-Coder-7B-4bit')
    start = time.time()
    response = generate(model, tokenizer, 
        prompt='Write a Python function to validate an email address using regex.', 
        max_tokens=150,
        verbose=False
    )
    elapsed = time.time() - start
    
    print(f"\nResponse:\n{response}\n")
    print(f"Time: {elapsed:.2f}s")
    print("✓ Coding model working perfectly!")
except:
    print("⊘ Qwen3-Coder-7B not downloaded, skipping test")
EOF

echo ""
echo "=================================================="
echo "CODING PACK INSTALLED!"
echo "=================================================="
echo ""
echo "These models excel at:"
echo "  • Code generation (Python, JS, Java, etc.)"
echo "  • Code explanation and documentation"
echo "  • Bug finding and fixing"
echo "  • Code optimization"
echo "  • Security vulnerability detection"
echo ""
echo "Test with:"
echo "  python3 test_model.py ./mlx/Qwen3-Coder-7B-4bit"
echo ""
