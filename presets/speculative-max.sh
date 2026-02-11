#!/bin/bash
# Speculative Decoding - Maximum Speed Preset
# Optimized for maximum speed with 7 draft tokens
# Best for: Long generations, text completion, bulk processing

set -e

# Activate virtual environment
source /Users/jonathanmallinger/models/.venv/bin/activate

# Configuration
MODEL_PATH="/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-3B-abliterated"
DRAFT_MODEL_PATH="/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-0.5B-abliterated"
NUM_DRAFT_TOKENS=7
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

echo "============================================"
echo "Starting Speculative Decoding - MAX Mode"
echo "============================================"
echo "Main Model: Josiefied-Qwen2.5-3B"
echo "Draft Model: Josiefied-Qwen2.5-0.5B"
echo "Draft Tokens: $NUM_DRAFT_TOKENS (MAXIMUM)"
echo "Port: $PORT"
echo "============================================"
echo ""
echo "Server will be available at: http://localhost:$PORT"
echo "Test with: curl http://localhost:$PORT/v1/models"
echo ""
echo "Note: Maximum draft tokens may show diminishing returns"
echo "for some workloads. Monitor acceptance rate."
echo ""

# Start server
mlx_lm.server \
  --model "$MODEL_PATH" \
  --draft-model "$DRAFT_MODEL_PATH" \
  --num-draft-tokens $NUM_DRAFT_TOKENS \
  --port $PORT \
  --host $HOST
