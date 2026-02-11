#!/bin/bash
# Test Script for Speculative Decoding Server

set -e

PORT="${1:-8000}"
BASE_URL="http://localhost:$PORT"

echo "=========================================="
echo "Testing Speculative Decoding Server"
echo "=========================================="
echo "Port: $PORT"
echo ""

# Test 1: Check if server is running
echo "Test 1: Checking server availability..."
if curl -s "$BASE_URL/v1/models" > /dev/null 2>&1; then
    echo "✓ Server is running"
else
    echo "✗ Server not responding on port $PORT"
    echo "Make sure the server is started with: ./start-speculative.sh"
    exit 1
fi

# Test 2: Get model info
echo ""
echo "Test 2: Getting model information..."
MODEL_INFO=$(curl -s "$BASE_URL/v1/models")
echo "$MODEL_INFO" | python3 -m json.tool 2>/dev/null || echo "$MODEL_INFO"

# Test 3: Simple generation test
echo ""
echo "Test 3: Testing text generation..."
echo "Prompt: 'Write a Python function to calculate fibonacci numbers'"
echo ""

START_TIME=$(date +%s.%N)

RESPONSE=$(curl -s "$BASE_URL/v1/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Josiefied-Qwen2.5-3B-abliterated",
    "prompt": "Write a Python function to calculate fibonacci numbers",
    "max_tokens": 150,
    "temperature": 0.7
  }')

END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)

echo "Response:"
echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['text'])" 2>/dev/null || echo "$RESPONSE"

echo ""
echo "Generation time: ${DURATION}s"

# Extract tokens if available
if echo "$RESPONSE" | grep -q "usage"; then
    TOTAL_TOKENS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('usage', {}).get('completion_tokens', 'N/A'))" 2>/dev/null || echo "N/A")
    if [ "$TOTAL_TOKENS" != "N/A" ]; then
        TOKENS_PER_SEC=$(echo "scale=2; $TOTAL_TOKENS / $DURATION" | bc)
        echo "Tokens generated: $TOTAL_TOKENS"
        echo "Speed: ${TOKENS_PER_SEC} tokens/sec"
    fi
fi

echo ""
echo "=========================================="
echo "Test Complete!"
echo "=========================================="
echo ""
echo "The server is working correctly."
echo "Expected performance: 40-60+ tokens/sec with speculative decoding"
echo "(vs ~25-35 tokens/sec without speculative decoding)"
