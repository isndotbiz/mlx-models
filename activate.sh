#!/bin/bash
# Quick activation script for the MLX virtual environment
# Usage: source activate.sh

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✓ MLX virtual environment activated"
    echo ""
    echo "Python: $(which python3)"
    echo "MLX version: $(python3 -c 'import mlx; print(mlx.__version__)' 2>/dev/null || echo 'not found')"
    echo ""
    echo "Ready to use! Try:"
    echo "  ./download_models.sh"
    echo "  python3 test_model.py ./mlx/MODEL_NAME"
else
    echo "✗ Virtual environment not found at .venv/"
    echo "Run: python3 -m venv .venv"
fi
