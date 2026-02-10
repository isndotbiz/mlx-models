#!/bin/bash

# MLX Models Download Script for Security Research

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
fi
# Optimized for M4 Pro MacBook with 24GB RAM, 16 GPU cores

set -e  # Exit on error

echo "=========================================="
echo "MLX Models Download Script"
echo "Target: M4 Pro MacBook (24GB RAM)"
echo "=========================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")/mlx"

echo "Current directory: $(pwd)"
echo ""

# Install dependencies if needed
echo "Checking dependencies..."
if ! command -v huggingface-cli &> /dev/null; then
    echo "Installing huggingface-cli..."
    pip install huggingface-hub
fi

echo ""
echo "=========================================="
echo "HIGH PRIORITY MODELS (Recommended)"
echo "=========================================="
echo ""

echo "[1/5] Downloading Dolphin-Qwen2.5-7B-4bit (~4-5GB)..."
echo "Highly uncensored, excellent reasoning"
huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit --local-dir ./Dolphin-Qwen2.5-7B-4bit
echo "✓ Complete"
echo ""

echo "[2/5] Downloading NousResearch-Hermes-3-Llama-3.1-8B-4bit (~5GB)..."
echo "Minimal guardrails, strong instruction following"
huggingface-cli download mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit --local-dir ./Hermes-3-Llama-3.1-8B-4bit
echo "✓ Complete"
echo ""

echo "[3/5] Downloading Ministral-8B-Instruct-2410-4bit (~5GB)..."
echo "Fast inference, good for quick evaluations"
huggingface-cli download mlx-community/Ministral-8B-Instruct-2410-4bit --local-dir ./Ministral-8B-Instruct-2410-4bit
echo "✓ Complete"
echo ""

echo "[4/5] Downloading Qwen2.5-14B-Instruct-4bit (~8GB)..."
echo "Baseline for comparison against abliterated versions"
huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit --local-dir ./Qwen2.5-14B-Instruct-4bit
echo "✓ Complete"
echo ""

echo "[5/5] Downloading Llama-3.2-11B-Vision-Instruct-4bit (~7GB)..."
echo "Vision capabilities for multimodal testing"
huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-4bit --local-dir ./Llama-3.2-11B-Vision-Instruct-4bit
echo "✓ Complete"
echo ""

echo "=========================================="
echo "MEDIUM PRIORITY MODELS (Optional - Larger)"
echo "=========================================="
echo ""

read -p "Download larger models (32B, 14B)? This will use ~27GB additional space. (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[6/7] Downloading Qwen2.5-32B-Instruct-4bit (~18-19GB)..."
    echo "Very capable, will use most of your 24GB RAM"
    huggingface-cli download mlx-community/Qwen2.5-32B-Instruct-4bit --local-dir ./Qwen2.5-32B-Instruct-4bit
    echo "✓ Complete"
    echo ""
    
    echo "[7/7] Downloading DeepSeek-R1-Distill-Qwen-14B-4bit (~8-9GB)..."
    echo "Reasoning-focused, recent model"
    huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-14B-4bit --local-dir ./DeepSeek-R1-Distill-Qwen-14B-4bit
    echo "✓ Complete"
    echo ""
else
    echo "Skipping larger models."
fi

echo "=========================================="
echo "SPECIALIZED MODELS"
echo "=========================================="
echo ""

read -p "Download specialized coding model? (~4GB) (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading CodeQwen1.5-7B-Chat-4bit (~4GB)..."
    echo "Code generation with fewer content filters"
    huggingface-cli download mlx-community/CodeQwen1.5-7B-Chat-4bit --local-dir ./CodeQwen1.5-7B-Chat-4bit
    echo "✓ Complete"
    echo ""
else
    echo "Skipping specialized models."
fi

echo ""
echo "=========================================="
echo "DOWNLOAD COMPLETE!"
echo "=========================================="
echo ""
echo "Models installed in: $(pwd)"
echo ""
echo "Currently installed models:"
ls -d */ | grep -v "^\." || echo "No models found"
echo ""
echo "Next steps:"
echo "1. Install MLX: pip install mlx mlx-lm"
echo "2. Install LM Studio: https://lmstudio.ai/"
echo "3. Test a model: python3 -c \"from mlx_lm import load, generate; model, tokenizer = load('./mlx/Dolphin-Qwen2.5-7B-4bit'); print(generate(model, tokenizer, prompt='Test', max_tokens=50))\""
echo ""
echo "See MLX_MODELS_SETUP_GUIDE.md for detailed usage instructions"
echo ""
