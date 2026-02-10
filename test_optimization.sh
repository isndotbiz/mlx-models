#!/bin/bash

# MLX Optimization Test Script for M4 Pro
# Tests all your models to verify optimal performance

set -e

echo "=================================================="
echo "MLX Optimization Test for M4 Pro (24GB RAM)"
echo "=================================================="
echo ""

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ No virtual environment found!"
    exit 1
fi

echo ""
echo "Checking MLX installation..."
python3 -c "import mlx.core as mx; print(f'✓ MLX {mx.__version__} - Device: {mx.default_device()}')"
python3 -c "import mlx_lm; print(f'✓ mlx-lm {mlx_lm.__version__}')"

echo ""
echo "=================================================="
echo "Test 1: Ultra-Fast Model (1.7B)"
echo "=================================================="
python3 << 'EOF'
import time
from mlx_lm import load, generate

print("\nLoading Josiefied-Qwen3-1.7B-abliterated-v1-4bit...")
start_load = time.time()
model, tokenizer = load('./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit')
load_time = time.time() - start_load
print(f"✓ Loaded in {load_time:.2f}s")

prompt = "Explain what SQL injection is in 2 sentences."
print(f"\nPrompt: {prompt}")
print("\nGenerating...")

start_gen = time.time()
response = generate(model, tokenizer, prompt=prompt, max_tokens=80, verbose=False)
gen_time = time.time() - start_gen

# Estimate tokens (rough)
tokens_est = len(response.split()) * 1.3
tps = tokens_est / gen_time if gen_time > 0 else 0

print(f"\nResponse:\n{response}\n")
print(f"Generation time: {gen_time:.2f}s")
print(f"Estimated speed: {tps:.1f} tokens/second")

if tps > 50:
    print("✓ EXCELLENT performance!")
elif tps > 30:
    print("✓ Good performance")
else:
    print("⚠ Slower than expected - check LM Studio uses MLX engine")
EOF

echo ""
echo "=================================================="
echo "Test 2: Coding Model (7B)"
echo "=================================================="
python3 << 'EOF'
import time
from mlx_lm import load, generate

print("\nLoading WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx...")
start_load = time.time()
model, tokenizer = load('./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx')
load_time = time.time() - start_load
print(f"✓ Loaded in {load_time:.2f}s")

prompt = "Write a Python function to validate email format."
print(f"\nPrompt: {prompt}")
print("\nGenerating...")

start_gen = time.time()
response = generate(model, tokenizer, prompt=prompt, max_tokens=100, verbose=False)
gen_time = time.time() - start_gen

tokens_est = len(response.split()) * 1.3
tps = tokens_est / gen_time if gen_time > 0 else 0

print(f"\nResponse:\n{response}\n")
print(f"Generation time: {gen_time:.2f}s")
print(f"Estimated speed: {tps:.1f} tokens/second")

if tps > 35:
    print("✓ EXCELLENT performance!")
elif tps > 20:
    print("✓ Good performance")
else:
    print("⚠ Slower than expected")
EOF

echo ""
echo "=================================================="
echo "Test 3: High-Quality Model (14B)"
echo "=================================================="
python3 << 'EOF'
import time
from mlx_lm import load, generate

print("\nLoading Josiefied-Qwen3-14B-abliterated-v3-6bit...")
print("(This is your largest model - loading may take 10-15 seconds)")
start_load = time.time()
model, tokenizer = load('./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit')
load_time = time.time() - start_load
print(f"✓ Loaded in {load_time:.2f}s")

prompt = "Describe common web application vulnerabilities."
print(f"\nPrompt: {prompt}")
print("\nGenerating...")

start_gen = time.time()
response = generate(model, tokenizer, prompt=prompt, max_tokens=100, verbose=False)
gen_time = time.time() - start_gen

tokens_est = len(response.split()) * 1.3
tps = tokens_est / gen_time if gen_time > 0 else 0

print(f"\nResponse:\n{response}\n")
print(f"Generation time: {gen_time:.2f}s")
print(f"Estimated speed: {tps:.1f} tokens/second")

if tps > 15:
    print("✓ EXCELLENT performance for 14B model!")
elif tps > 10:
    print("✓ Good performance for 14B model")
else:
    print("⚠ Lower than expected - may need more RAM freed up")
EOF

echo ""
echo "=================================================="
echo "OPTIMIZATION TEST COMPLETE"
echo "=================================================="
echo ""
echo "Summary:"
echo "--------"
echo "Your M4 Pro performance targets:"
echo "  • 1.7B model: Should hit 80-120 tokens/s"
echo "  • 7B model:   Should hit 40-60 tokens/s"
echo "  • 14B model:  Should hit 15-25 tokens/s"
echo ""
echo "Next steps:"
echo "1. Open LM Studio: open '/Applications/LM Studio.app'"
echo "2. Set inference engine to 'MLX (Apple Silicon GPU)'"
echo "3. Point LM Studio to your models at: $PWD/mlx"
echo "4. Start testing for your security research class!"
echo ""
echo "See OPTIMIZATION_GUIDE.md for detailed tuning tips."
echo ""
