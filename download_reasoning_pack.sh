#!/bin/bash

# Download Reasoning Models Pack
# DeepSeek R1 series - Latest reasoning models

set -e
source .venv/bin/activate

echo "=================================================="
echo "Reasoning Models Pack (DeepSeek R1)"
echo "=================================================="
echo ""
echo "This will download:"
echo "  1. DeepSeek-R1-Distill-Qwen-1.5B-3bit (1GB) - Ultra-fast ⚡"
echo "  2. DeepSeek-R1-Distill-Qwen-7B (5GB) - Balanced ⭐"
echo "  3. DeepSeek-R1-0528-Qwen3-8B-8bit (8GB) - High quality"
echo "  4. DeepSeek-R1-Distill-Qwen-32B-4bit (19GB) - Maximum 🏆"
echo "  5. QwQ-32B-4bit (19GB) - Apache 2 licensed"
echo ""
echo "Total: ~52GB (select which ones to download)"
echo ""

read -p "Download all? (y/N): " -n 1 -r
echo ""
ALL=$REPLY

cd mlx

echo ""
echo "[1/5] DeepSeek-R1-Distill-Qwen-1.5B-3bit"
echo "   ⚡ ULTRA-FAST - 120+ tokens/s"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-1.5B-3bit \
      --local-dir ./DeepSeek-R1-Distill-Qwen-1.5B-3bit
    echo "✓ Complete"
else
    read -p "  Download this model? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-1.5B-3bit \
          --local-dir ./DeepSeek-R1-Distill-Qwen-1.5B-3bit
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

echo ""
echo "[2/5] DeepSeek-R1-Distill-Qwen-7B"
echo "   ⭐ BEST BALANCE - Efficient reasoning"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-7B \
      --local-dir ./DeepSeek-R1-Distill-Qwen-7B
    echo "✓ Complete"
else
    read -p "  Download this model? (Y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-7B \
          --local-dir ./DeepSeek-R1-Distill-Qwen-7B
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

echo ""
echo "[3/5] DeepSeek-R1-0528-Qwen3-8B-8bit"
echo "   💎 HIGH QUALITY - 8-bit precision"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download mlx-community/DeepSeek-R1-0528-Qwen3-8B-8bit \
      --local-dir ./DeepSeek-R1-0528-Qwen3-8B-8bit
    echo "✓ Complete"
else
    read -p "  Download this model? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        huggingface-cli download mlx-community/DeepSeek-R1-0528-Qwen3-8B-8bit \
          --local-dir ./DeepSeek-R1-0528-Qwen3-8B-8bit
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

echo ""
echo "[4/5] DeepSeek-R1-Distill-Qwen-32B-4bit"
echo "   🏆 MAXIMUM QUALITY - Near GPT-4 reasoning"
echo "   ⚠ Warning: Uses 19GB, leaves only 5GB for system"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit \
      --local-dir ./DeepSeek-R1-Distill-Qwen-32B-4bit
    echo "✓ Complete"
else
    read -p "  Download this model? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit \
          --local-dir ./DeepSeek-R1-Distill-Qwen-32B-4bit
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

echo ""
echo "[5/5] QwQ-32B-4bit"
echo "   📜 Apache 2 licensed, 128K context"
echo "   ⚠ Warning: Uses 19GB, leaves only 5GB for system"
if [[ $ALL =~ ^[Yy]$ ]]; then
    huggingface-cli download lmstudio-community/QwQ-32B-MLX-4bit \
      --local-dir ./QwQ-32B-4bit
    echo "✓ Complete"
else
    read -p "  Download this model? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        huggingface-cli download lmstudio-community/QwQ-32B-MLX-4bit \
          --local-dir ./QwQ-32B-4bit
        echo "✓ Complete"
    else
        echo "⊘ Skipped"
    fi
fi

cd ..

echo ""
echo "=================================================="
echo "REASONING PACK INSTALLED!"
echo "=================================================="
echo ""
echo "DeepSeek R1 models are specialized for:"
echo "  • Complex problem solving"
echo "  • Mathematical reasoning"
echo "  • Code analysis"
echo "  • Multi-step logical tasks"
echo ""
echo "Test with:"
echo "  python3 test_model.py ./mlx/DeepSeek-R1-Distill-Qwen-7B"
echo ""
