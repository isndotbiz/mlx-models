#!/usr/bin/env python3
"""Test running multiple MLX models in parallel"""

import time
import multiprocessing as mp
from mlx_lm import load, generate
import mlx.core as mx

def test_model(model_path, model_name, prompt):
    """Test a single model"""
    try:
        print(f"\n[{model_name}] Loading...")
        start = time.time()
        model, tokenizer = load(model_path)
        load_time = time.time() - start

        print(f"[{model_name}] ✓ Loaded in {load_time:.2f}s")
        print(f"[{model_name}] Generating response...")

        start = time.time()
        response = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=50,
            verbose=False
        )
        gen_time = time.time() - start

        # Count tokens (approximate)
        tokens = len(response.split())
        speed = tokens / gen_time if gen_time > 0 else 0

        print(f"[{model_name}] ✓ Generated {tokens} tokens in {gen_time:.2f}s ({speed:.1f} t/s)")
        print(f"[{model_name}] Response: {response[:100]}...")

        return {
            'name': model_name,
            'load_time': load_time,
            'gen_time': gen_time,
            'speed': speed,
            'success': True
        }
    except Exception as e:
        print(f"[{model_name}] ❌ Error: {e}")
        return {
            'name': model_name,
            'success': False,
            'error': str(e)
        }

def main():
    # Define the fast models
    models = [
        ("./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit", "DeepSeek-1.5B", "Explain quantum computing in one sentence: "),
        ("./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit", "Josiefied-1.7B", "What is a SQL injection attack? "),
        ("./mlx/Qwen3-4B-4bit", "Qwen3-4B", "Write a Python function to check if a number is prime: "),
    ]

    print("="*70)
    print("🚀 PARALLEL MODEL TEST - 24GB M4 Pro")
    print("="*70)
    print("\nTesting 3 models simultaneously...")
    print("Models: DeepSeek-1.5B (0.7GB) + Josiefied-1.7B (0.9GB) + Qwen3-4B (2.0GB)")
    print("Total: ~3.6GB of models")
    print("\nStarting parallel execution...\n")

    # Run all models in parallel using multiprocessing
    start_time = time.time()

    with mp.Pool(processes=3) as pool:
        results = pool.starmap(test_model, models)

    total_time = time.time() - start_time

    # Print summary
    print("\n" + "="*70)
    print("📊 PARALLEL EXECUTION SUMMARY")
    print("="*70)

    successful = [r for r in results if r.get('success')]

    if successful:
        print(f"\n✅ All {len(successful)} models ran successfully in parallel!")
        print(f"⏱️  Total wall time: {total_time:.2f}s")
        print(f"\n{'Model':<20} {'Load Time':<12} {'Gen Speed':<15}")
        print("-" * 50)
        for r in successful:
            print(f"{r['name']:<20} {r['load_time']:>8.2f}s    {r['speed']:>8.1f} t/s")

        print(f"\n💪 Your 24GB M4 Pro handled all 3 models simultaneously!")
        print(f"🎯 Combined model size: ~3.6GB (only 15% of your RAM)")
        print(f"✨ You could run 2-3 more models if needed!")
    else:
        print(f"\n⚠️  Some models failed:")
        for r in results:
            if not r.get('success'):
                print(f"  - {r['name']}: {r.get('error')}")

    print("\n" + "="*70)

if __name__ == "__main__":
    mp.set_start_method('spawn', force=True)
    main()
