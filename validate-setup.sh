#!/bin/bash
# Validate Speculative Decoding Setup

set -e

echo "=========================================="
echo "Speculative Decoding Setup Validation"
echo "=========================================="
echo ""

ERRORS=0

# Check virtual environment
echo "1. Checking virtual environment..."
if [ -d "/Users/jonathanmallinger/models/.venv" ]; then
    echo "   ✓ Virtual environment exists"
else
    echo "   ✗ Virtual environment not found"
    ERRORS=$((ERRORS + 1))
fi

# Check mlx_lm.server in venv
if [ -f "/Users/jonathanmallinger/models/.venv/bin/mlx_lm.server" ]; then
    echo "   ✓ mlx_lm.server installed"
else
    echo "   ✗ mlx_lm.server not found"
    ERRORS=$((ERRORS + 1))
fi

# Check models exist
echo ""
echo "2. Checking models..."
if [ -d "/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-3B-abliterated" ]; then
    echo "   ✓ Main model (3B) exists"
else
    echo "   ✗ Main model (3B) not found"
    ERRORS=$((ERRORS + 1))
fi

if [ -d "/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-0.5B-abliterated" ]; then
    echo "   ✓ Draft model (0.5B) exists"
else
    echo "   ✗ Draft model (0.5B) not found"
    ERRORS=$((ERRORS + 1))
fi

# Check preset scripts
echo ""
echo "3. Checking preset scripts..."
for preset in fast balanced max; do
    if [ -x "/Users/jonathanmallinger/models/presets/speculative-$preset.sh" ]; then
        echo "   ✓ speculative-$preset.sh (executable)"
    else
        echo "   ✗ speculative-$preset.sh missing or not executable"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check system prompts
echo ""
echo "4. Checking system prompts..."
for prompt in anti-refusal expert empty; do
    if [ -f "/Users/jonathanmallinger/models/presets/prompts/$prompt.txt" ]; then
        echo "   ✓ $prompt.txt exists"
    else
        echo "   ✗ $prompt.txt not found"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check main scripts
echo ""
echo "5. Checking main scripts..."
for script in start-speculative test-speculative stop-server; do
    if [ -x "/Users/jonathanmallinger/models/$script.sh" ]; then
        echo "   ✓ $script.sh (executable)"
    else
        echo "   ✗ $script.sh missing or not executable"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check documentation
echo ""
echo "6. Checking documentation..."
if [ -f "/Users/jonathanmallinger/models/QUICK_START_SPECULATIVE.md" ]; then
    echo "   ✓ QUICK_START_SPECULATIVE.md exists"
else
    echo "   ✗ QUICK_START_SPECULATIVE.md not found"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "/Users/jonathanmallinger/models/presets/README.md" ]; then
    echo "   ✓ presets/README.md exists"
else
    echo "   ✗ presets/README.md not found"
    ERRORS=$((ERRORS + 1))
fi

# Check OpenCode config
echo ""
echo "7. Checking OpenCode configuration..."
if [ -f "/Users/jonathanmallinger/.config/opencode/opencode.json" ]; then
    echo "   ✓ OpenCode config exists"

    if grep -q "qwen2.5-3b-speculative-balanced" "/Users/jonathanmallinger/.config/opencode/opencode.json"; then
        echo "   ✓ Speculative balanced model configured"
    else
        echo "   ⚠ Speculative balanced model not found in config"
    fi

    if grep -q "qwen2.5-3b-speculative-fast" "/Users/jonathanmallinger/.config/opencode/opencode.json"; then
        echo "   ✓ Speculative fast model configured"
    else
        echo "   ⚠ Speculative fast model not found in config"
    fi

    if grep -q "qwen2.5-3b-speculative-max" "/Users/jonathanmallinger/.config/opencode/opencode.json"; then
        echo "   ✓ Speculative max model configured"
    else
        echo "   ⚠ Speculative max model not found in config"
    fi
else
    echo "   ✗ OpenCode config not found"
    ERRORS=$((ERRORS + 1))
fi

# Check port availability
echo ""
echo "8. Checking port availability..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    PID=$(lsof -Pi :8000 -sTCP:LISTEN -t)
    echo "   ⚠ Port 8000 is in use (PID: $PID)"
    echo "     Will fall back to port 8080"
else
    echo "   ✓ Port 8000 available"
fi

if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    PID=$(lsof -Pi :8080 -sTCP:LISTEN -t)
    echo "   ⚠ Port 8080 is in use (PID: $PID)"
else
    echo "   ✓ Port 8080 available"
fi

# Summary
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo "✓ Setup validation PASSED!"
    echo "=========================================="
    echo ""
    echo "Everything is configured correctly."
    echo ""
    echo "Next steps:"
    echo "  1. Start server: ./start-speculative.sh"
    echo "  2. Test it:      ./test-speculative.sh"
    echo "  3. Stop server:  ./stop-server.sh"
    echo ""
    echo "Or use with OpenCode (it's already configured!)."
    exit 0
else
    echo "✗ Setup validation FAILED with $ERRORS error(s)"
    echo "=========================================="
    echo ""
    echo "Please review the errors above and fix them."
    exit 1
fi
