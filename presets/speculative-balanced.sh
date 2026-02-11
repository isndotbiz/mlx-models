#!/bin/bash
# Speculative Decoding - Balanced Preset
# Optimized for best balance of speed and quality with 5 draft tokens
# Best for: General use, coding assistance, most tasks

set -e

# Activate virtual environment
source /Users/jonathanmallinger/models/.venv/bin/activate

# Configuration
MODEL_PATH="/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-3B-abliterated"
DRAFT_MODEL_PATH="/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-0.5B-abliterated"
NUM_DRAFT_TOKENS=5
PORT=8000
HOST="0.0.0.0"

# Try primary port, fall back to 8080 if busy
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "Port $PORT is busy, trying 8080..."
    PORT=8080
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "Error: Both ports 8000 and 8080 are busy"
        exit 1
    fi
fi

echo "================================================"
echo "Starting Speculative Decoding - BALANCED Mode"
echo "================================================"
echo "Main Model: Josiefied-Qwen2.5-3B"
echo "Draft Model: Josiefied-Qwen2.5-0.5B"
echo "Draft Tokens: $NUM_DRAFT_TOKENS (RECOMMENDED)"
echo "Port: $PORT"
echo "================================================"
echo ""
echo "Server will be available at: http://localhost:$PORT"
echo "Test with: curl http://localhost:$PORT/v1/models"
echo ""

# Start server
mlx_lm.server \
  --model "$MODEL_PATH" \
  --draft-model "$DRAFT_MODEL_PATH" \
  --num-draft-tokens $NUM_DRAFT_TOKENS \
  --port $PORT \
  --host $HOST
