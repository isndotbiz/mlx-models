#!/bin/bash

# Download Uncensored/Abliterated Models Pack
# Optimized for M4 Pro 24GB - Security Research

set -e
source .venv/bin/activate

echo "=================================================="
echo "Uncensored Models Pack for Security Research"
echo "=================================================="
echo ""
echo "This will download:"
echo "  1. Josiefied-Qwen3-8B-abliterated (5GB) - Balanced ⭐"
echo "  2. Josiefied-Qwen3-4B-abliterated (2.5GB) - Fast"
echo "  3. Josiefied-DeepSeek-R1-8B-abliterated (5GB) - Reasoning"
echo "  4. Llama-3.1-8B-abliterated (8GB) - High quality"
echo "  5. Llama-3.2-11B-Vision-abliterated (7GB) - Vision!"
echo ""
echo "Total: ~27GB"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

cd mlx

echo ""
echo "[1/5] Josiefied-Qwen3-8B-abliterated-v1-4bit"
echo "   ⭐ BEST BALANCED - Fast & capable"
huggingface-cli download mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --local-dir ./Josiefied-Qwen3-8B-abliterated-v1-4bit
echo "✓ Complete"

echo ""
echo "[2/5] Josiefied-Qwen3-4B-abliterated-v1-4bit"
echo "   ⚡ FASTEST - 80-100 tokens/s"
huggingface-cli download mlx-community/Josiefied-Qwen3-4B-abliterated-v1-4bit \
  --local-dir ./Josiefied-Qwen3-4B-abliterated-v1-4bit
echo "✓ Complete"

echo ""
echo "[3/5] Josiefied-DeepSeek-R1-0528-Qwen3-8B-abliterated"
echo "   🧠 REASONING - Uncensored problem solving"
huggingface-cli download mlx-community/Josiefied-DeepSeek-R1-0528-Qwen3-8B-abliterated-v1-4bit \
  --local-dir ./Josiefied-DeepSeek-R1-8B-abliterated
echo "✓ Complete"

echo ""
echo "[4/5] Meta-Llama-3.1-8B-Instruct-abliterated-8bit"
echo "   💎 HIGH QUALITY - 8-bit quantization"
huggingface-cli download mlx-community/Meta-Llama-3.1-8B-Instruct-abliterated-8bit \
  --local-dir ./Llama-3.1-8B-abliterated-8bit
echo "✓ Complete"

echo ""
echo "[5/5] Llama-3.2-11B-Vision-abliterated-4bit"
echo "   👁️ VISION - Uncensored multimodal!"
huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-abliterated-4-bit \
  --local-dir ./Llama-3.2-11B-Vision-abliterated-4bit
echo "✓ Complete"

cd ..

echo ""
echo "=================================================="
echo "Testing new models..."
echo "=================================================="

# Quick test of one model
echo ""
echo "Quick test of Josiefied-Qwen3-8B..."
source .venv/bin/activate
python3 << 'EOF'
from mlx_lm import load, generate
import time

model, tokenizer = load('./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit')
start = time.time()
response = generate(model, tokenizer, 
    prompt='Explain SQL injection vulnerabilities in 2 sentences.', 
    max_tokens=80,
    verbose=False
)
elapsed = time.time() - start
tokens_est = len(response.split()) * 1.3
tps = tokens_est / elapsed if elapsed > 0 else 0

print(f"\nResponse: {response}\n")
print(f"Speed: {tps:.1f} tokens/second")
print("✓ Working perfectly!" if tps > 40 else "⚠ Check configuration")
EOF

echo ""
echo "=================================================="
echo "UNCENSORED PACK INSTALLED!"
echo "=================================================="
echo ""
echo "Your uncensored models:"
echo "  ✓ Josiefied-Qwen3-1.7B (already had) - 938MB"
echo "  ✓ Josiefied-Qwen3-4B (new) - 2.5GB"
echo "  ✓ Josiefied-Qwen3-8B (new) - 5GB ⭐"
echo "  ✓ Josiefied-DeepSeek-R1-8B (new) - 5GB"
echo "  ✓ Llama-3.1-8B-abliterated (new) - 8GB"
echo "  ✓ Llama-3.2-11B-Vision (new) - 7GB"
echo ""
echo "Start testing:"
echo "  python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit"
echo ""
echo "Or use in LM Studio:"
echo "  open '/Applications/LM Studio.app'"
echo "  Set engine to: MLX (Apple Silicon GPU)"
echo ""
