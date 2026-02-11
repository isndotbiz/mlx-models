#!/bin/bash
# Quick Start Script for Speculative Decoding
# Default: Balanced preset (5 draft tokens)

set -e

PRESET="${1:-balanced}"
SCRIPT_DIR="/Users/jonathanmallinger/models/presets"

echo "=========================================="
echo "Speculative Decoding Quick Start"
echo "=========================================="
echo ""

case "$PRESET" in
    fast)
        echo "Starting FAST preset (3 draft tokens)..."
        exec "$SCRIPT_DIR/speculative-fast.sh"
        ;;
    balanced)
        echo "Starting BALANCED preset (5 draft tokens) [RECOMMENDED]..."
        exec "$SCRIPT_DIR/speculative-balanced.sh"
        ;;
    max)
        echo "Starting MAX preset (7 draft tokens)..."
        exec "$SCRIPT_DIR/speculative-max.sh"
        ;;
    *)
        echo "Unknown preset: $PRESET"
        echo ""
        echo "Usage: $0 [fast|balanced|max]"
        echo ""
        echo "Presets:"
        echo "  fast     - 3 draft tokens (quick responses)"
        echo "  balanced - 5 draft tokens (recommended)"
        echo "  max      - 7 draft tokens (maximum speed)"
        echo ""
        echo "Default: balanced"
        exit 1
        ;;
esac
