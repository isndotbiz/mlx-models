#!/bin/bash
# OpenCode CLI Wrapper - Claude Code Compatible
# Usage: ./opencode_cli.sh "your prompt here" [primary|speculative]

set -e

ENDPOINT="${2:-primary}"
PROMPT="$1"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 \"your prompt\" [primary|speculative]"
    echo ""
    echo "Endpoints:"
    echo "  primary      - Josiefied 8B @ localhost:1234 (40 tok/s)"
    echo "  speculative  - Qwen2.5 3B @ localhost:8000 (60-120 tok/s)"
    exit 1
fi

# Select endpoint
if [ "$ENDPOINT" = "speculative" ]; then
    URL="http://localhost:8000/v1/chat/completions"
    MODEL="/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-3B-abliterated"
else
    URL="http://localhost:1234/v1/chat/completions"
    MODEL="josiefied-qwen3-8b-abliterated-v1"
fi

echo "========================================"
echo "OpenCode CLI (Claude Code Compatible)"
echo "========================================"
echo "Endpoint: $ENDPOINT"
echo "Model: $MODEL"
echo "Max Tokens: 2048"
echo "========================================"
echo ""

# Make request with proper formatting
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are an AI coding assistant. Use ''' delimiters between answers. Be direct and concise. Max 2048 tokens per response.\"
      },
      {
        \"role\": \"user\",
        \"content\": $(echo "$PROMPT" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))")
      }
    ],
    \"max_tokens\": 2048,
    \"temperature\": 0.7,
    \"top_p\": 0.9,
    \"stream\": false
  }" | python3 -c "
import sys, json
data = json.load(sys.stdin)
content = data['choices'][0]['message']['content']
delimiter = \"'''\"
print(f'\n{delimiter}\n{content}\n{delimiter}')
print()
print('---')
print(f\"Tokens: {data['usage']['total_tokens']} (prompt: {data['usage']['prompt_tokens']}, completion: {data['usage']['completion_tokens']})\")
"

echo ""
echo "========================================"
