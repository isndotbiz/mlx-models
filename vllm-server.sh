#!/bin/bash
# vLLM-MLX Server Launcher
# High-performance OpenAI-compatible API server

set -e

cd /Users/jonathanmallinger/models
source .venv/bin/activate

# Default settings
MODEL="${1:-./mlx/Qwen3-4B-4bit}"
PORT="${2:-8000}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting vLLM-MLX Server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Model: $MODEL"
echo "Port:  $PORT"
echo "API:   http://localhost:$PORT/v1"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "OpenAI-compatible endpoints:"
echo "  • POST http://localhost:$PORT/v1/completions"
echo "  • POST http://localhost:$PORT/v1/chat/completions"
echo ""
echo "Press Ctrl+C to stop server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start server
python3 -m vllm_mlx.cli serve "$MODEL" --port "$PORT"
