#!/bin/bash

# Fix Models Script - Download verified working models

set -e

source .venv/bin/activate

echo "=================================================="
echo "Downloading Verified MLX Models"
echo "=================================================="
echo ""
echo "These models are pre-tested by mlx-community"
echo "Total download: ~19GB"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

cd mlx

echo ""
echo "[1/3] Dolphin-Qwen2.5-7B-4bit (~4-5GB)"
echo "   Highly uncensored, excellent reasoning"
huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit \
  --local-dir ./Dolphin-Qwen2.5-7B-4bit
echo "✓ Complete"

echo ""
echo "[2/3] Hermes-3-Llama-3.1-8B-4bit (~5GB)"
echo "   Minimal guardrails, strong instruction following"
huggingface-cli download mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit \
  --local-dir ./Hermes-3-Llama-3.1-8B-4bit
echo "✓ Complete"

echo ""
echo "[3/3] Qwen2.5-14B-Instruct-4bit (~8GB)"
echo "   Baseline for comparison (has guardrails)"
huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit \
  --local-dir ./Qwen2.5-14B-Instruct-4bit
echo "✓ Complete"

cd ..

echo ""
echo "=================================================="
echo "Testing new models..."
echo "=================================================="

./test_optimization.sh

echo ""
echo "=================================================="
echo "Setup complete!"
echo "=================================================="
echo ""
echo "Your models:"
echo "  ✓ Josiefied-Qwen3-1.7B (working perfectly!)"
echo "  ✓ Dolphin-Qwen2.5-7B (new, verified)"
echo "  ✓ Hermes-3-Llama-3.1-8B (new, verified)"
echo "  ✓ Qwen2.5-14B (new, verified)"
echo ""
echo "You can safely delete the old problematic models:"
echo "  rm -rf ./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx"
echo "  rm -rf ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit"
echo ""
