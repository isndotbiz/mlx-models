#!/bin/bash
# Start the MLX LM Server for 30B models
# Usage: ./mlx-server/start.sh [--model MODEL] [--thinking]
#
# Default: josiefied-qwen3-30b-a3b-abliterated on port 8080, thinking disabled
# With thinking: ./mlx-server/start.sh --thinking
# Coder model: ./mlx-server/start.sh --model qwen3-coder-30b-a3b

DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$DIR/.venv/bin/python3"
SERVER="$DIR/server.py"

MODEL="josiefied-qwen3-30b-a3b-abliterated"
PORT=8080
NO_THINKING="--no-thinking"

while [[ $# -gt 0 ]]; do
    case $1 in
        --model) MODEL="$2"; shift 2 ;;
        --thinking) NO_THINKING=""; shift ;;
        --port) PORT="$2"; shift 2 ;;
        *) shift ;;
    esac
done

echo "Starting MLX LM Server..."
echo "  Model: $MODEL"
echo "  Port: $PORT"
echo "  Thinking: $([ -z "$NO_THINKING" ] && echo 'enabled' || echo 'disabled')"
echo ""

exec "$PYTHON" "$SERVER" --model "$MODEL" --port "$PORT" $NO_THINKING
