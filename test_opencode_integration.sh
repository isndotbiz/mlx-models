#!/bin/bash
# OpenCode Integration Test Script
# Tests both MLX and LM Studio providers

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         OpenCode Integration Test                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Check if servers are running
echo "🔍 Test 1: Checking Server Status..."
echo ""

echo "  MLX Server (11434):"
if curl -s http://localhost:11434/v1/models > /dev/null 2>&1; then
    echo "    ✅ Running"
    MODEL_COUNT=$(curl -s http://localhost:11434/v1/models | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']))")
    echo "    📊 Models available: $MODEL_COUNT"
else
    echo "    ❌ Not running"
    echo "    Start with: cd ~/workspace/llm-security-research && ./start-mlx-server.sh"
    exit 1
fi

echo ""
echo "  LM Studio Server (1234):"
if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "    ✅ Running"
    MODEL_COUNT=$(curl -s http://localhost:1234/v1/models | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']))")
    echo "    📊 Models available: $MODEL_COUNT"
else
    echo "    ❌ Not running"
    echo "    Start LM Studio and click 'Start Server'"
    exit 1
fi

echo ""
echo "─────────────────────────────────────────────────────────────────"

# Test 2: OpenCode configuration
echo ""
echo "🔍 Test 2: Checking OpenCode Configuration..."
echo ""

if [ -f ~/.opencode/config.json ]; then
    echo "  ✅ Config file exists"
    if grep -q '"mlx"' ~/.opencode/config.json && grep -q '"lmstudio"' ~/.opencode/config.json; then
        echo "  ✅ Both providers configured"
    else
        echo "  ❌ Missing provider configuration"
        exit 1
    fi
else
    echo "  ❌ Config file not found"
    exit 1
fi

echo ""
echo "─────────────────────────────────────────────────────────────────"

# Test 3: OpenCode models listing
echo ""
echo "🔍 Test 3: Testing OpenCode Models Command..."
echo ""

echo "  MLX Models:"
MLX_MODELS=$(opencode models mlx | wc -l | tr -d ' ')
echo "    ✅ Found $MLX_MODELS models"

echo ""
echo "  LM Studio Models:"
LMSTUDIO_MODELS=$(opencode models lmstudio | wc -l | tr -d ' ')
echo "    ✅ Found $LMSTUDIO_MODELS models"

echo ""
echo "─────────────────────────────────────────────────────────────────"

# Test 4: API Test - MLX
echo ""
echo "🔍 Test 4: Testing MLX Chat Completion..."
echo ""

START=$(date +%s)
RESPONSE=$(curl -s -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"josiefied-qwen2.5-0.5b","messages":[{"role":"user","content":"Say hello in one word."}],"max_tokens":10}')
END=$(date +%s)
TIME=$((END - START))

if echo "$RESPONSE" | grep -q '"content"'; then
    echo "  ✅ Chat completion successful"
    echo "  ⏱️  Response time: ${TIME}s"
    CONTENT=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'][:50])")
    echo "  💬 Response: $CONTENT"
else
    echo "  ❌ Chat completion failed"
    exit 1
fi

echo ""
echo "─────────────────────────────────────────────────────────────────"

# Test 5: API Test - LM Studio
echo ""
echo "🔍 Test 5: Testing LM Studio Chat Completion..."
echo ""

START=$(date +%s)
RESPONSE=$(curl -s -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"josiefied-qwen3-8b-abliterated-v1","messages":[{"role":"user","content":"Say hello in one word."}],"max_tokens":10}')
END=$(date +%s)
TIME=$((END - START))

if echo "$RESPONSE" | grep -q '"content"'; then
    echo "  ✅ Chat completion successful"
    echo "  ⏱️  Response time: ${TIME}s"
    CONTENT=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'][:50])")
    echo "  💬 Response: $CONTENT"
else
    echo "  ❌ Chat completion failed"
    exit 1
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  ALL TESTS PASSED ✅                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "  • MLX Server: Running with $MLX_MODELS models"
echo "  • LM Studio: Running with $LMSTUDIO_MODELS models"
echo "  • OpenCode: Configured for both providers"
echo "  • API Tests: Both providers responding correctly"
echo ""
echo "🎉 OpenCode integration is fully operational!"
echo ""
