#!/usr/bin/env python3
"""Comprehensive benchmark of all small models"""

import time
import json
from mlx_lm import load, generate
import mlx.core as mx

# Small models to benchmark (under 3GB)
MODELS = [
    ("./mlx/Josiefied-Qwen2.5-0.5B-abliterated", "Qwen 0.5B", 0.278),
    ("./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit", "DeepSeek 1.5B", 0.7),
    ("./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit", "Qwen 1.7B", 0.9),
    ("./mlx/Josiefied-Qwen2.5-3B-abliterated", "Qwen 3B", 1.74),
    ("./mlx/Qwen3-4B-4bit", "Qwen3 4B", 2.0),
    ("./mlx/gemma-3-4b-abliterated", "Gemma 4B", 2.56),
]

# Test prompts (security research focus)
TEST_PROMPTS = [
    "What is SQL injection?",
    "Explain XSS attacks in one sentence:",
    "Write a Python function to validate email addresses:",
]

def benchmark_model(model_path, model_name, model_size_gb):
    """Benchmark a single model"""
    results = {
        'name': model_name,
        'path': model_path,
        'size_gb': model_size_gb,
        'load_time': 0,
        'tests': []
    }

    print(f"\n{'='*70}")
    print(f"📊 Benchmarking: {model_name} ({model_size_gb}GB)")
    print(f"{'='*70}")

    try:
        # Load model
        print("Loading model...", flush=True)
        load_start = time.time()
        model, tokenizer = load(model_path)
        load_time = time.time() - load_start
        results['load_time'] = load_time

        print(f"✓ Loaded in {load_time:.2f}s")

        # Warmup
        print("Warming up...", flush=True)
        for _ in range(3):
            _ = generate(model, tokenizer, prompt="test", max_tokens=5, verbose=False)

        # Run tests
        for i, prompt in enumerate(TEST_PROMPTS, 1):
            print(f"\nTest {i}/{len(TEST_PROMPTS)}: {prompt[:40]}...", flush=True)

            mx.metal.reset_peak_memory()

            start = time.time()
            response = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=50,
                verbose=False
            )
            gen_time = time.time() - start

            # Calculate metrics
            tokens = len(tokenizer.encode(response))
            throughput = tokens / gen_time if gen_time > 0 else 0
            peak_memory = mx.metal.get_peak_memory() / (1024**3)

            test_result = {
                'prompt': prompt,
                'tokens': tokens,
                'time': gen_time,
                'throughput': throughput,
                'memory_gb': peak_memory,
                'response': response[:100]
            }

            results['tests'].append(test_result)
            print(f"  Speed: {throughput:.1f} tok/s | Memory: {peak_memory:.2f}GB")

        # Calculate averages
        avg_throughput = sum(t['throughput'] for t in results['tests']) / len(results['tests'])
        avg_memory = sum(t['memory_gb'] for t in results['tests']) / len(results['tests'])

        results['avg_throughput'] = avg_throughput
        results['avg_memory'] = avg_memory
        results['success'] = True

        print(f"\n✅ Average: {avg_throughput:.1f} tok/s | {avg_memory:.2f}GB memory")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        results['success'] = False
        results['error'] = str(e)

    return results

def main():
    print("╔" + "═"*68 + "╗")
    print("║" + "  COMPREHENSIVE SMALL MODEL BENCHMARK - M4 Pro 24GB".center(68) + "║")
    print("╚" + "═"*68 + "╝")

    print(f"\nBenchmarking {len(MODELS)} models with {len(TEST_PROMPTS)} test prompts each")
    print(f"Total tests: {len(MODELS) * len(TEST_PROMPTS)}")

    # Run benchmarks
    all_results = []
    total_start = time.time()

    for model_path, model_name, model_size in MODELS:
        result = benchmark_model(model_path, model_name, model_size)
        all_results.append(result)

    total_time = time.time() - total_start

    # Summary report
    print("\n" + "="*70)
    print("📈 BENCHMARK SUMMARY")
    print("="*70)

    # Sort by throughput
    successful = [r for r in all_results if r.get('success', False)]
    successful.sort(key=lambda x: x['avg_throughput'], reverse=True)

    print(f"\n{'Rank':<6} {'Model':<20} {'Size':<8} {'Speed':<12} {'Memory':<10} {'Load'}")
    print("-"*70)

    for i, r in enumerate(successful, 1):
        print(f"{i:<6} {r['name']:<20} {r['size_gb']:<7.2f}G "
              f"{r['avg_throughput']:>7.1f} t/s  {r['avg_memory']:>6.2f} GB  "
              f"{r['load_time']:>5.2f}s")

    # Best in class
    print("\n" + "="*70)
    print("🏆 BEST IN CLASS")
    print("="*70)

    if successful:
        fastest = max(successful, key=lambda x: x['avg_throughput'])
        smallest = min(successful, key=lambda x: x['size_gb'])
        most_efficient = min(successful, key=lambda x: x['avg_memory'])

        print(f"\n⚡ Fastest:         {fastest['name']:<20} {fastest['avg_throughput']:.1f} tok/s")
        print(f"📦 Smallest:        {smallest['name']:<20} {smallest['size_gb']:.2f} GB")
        print(f"💾 Most Efficient:  {most_efficient['name']:<20} {most_efficient['avg_memory']:.2f} GB memory")

        # Value ranking (speed per GB)
        for r in successful:
            r['value_score'] = r['avg_throughput'] / r['size_gb']

        best_value = max(successful, key=lambda x: x['value_score'])
        print(f"💎 Best Value:      {best_value['name']:<20} {best_value['value_score']:.1f} tok/s per GB")

    # Speed tiers
    print("\n" + "="*70)
    print("📊 SPEED TIERS")
    print("="*70)

    ultra_fast = [r for r in successful if r['avg_throughput'] >= 100]
    fast = [r for r in successful if 50 <= r['avg_throughput'] < 100]
    standard = [r for r in successful if r['avg_throughput'] < 50]

    if ultra_fast:
        print(f"\n⚡⚡⚡ ULTRA FAST (100+ tok/s):")
        for r in sorted(ultra_fast, key=lambda x: x['avg_throughput'], reverse=True):
            print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} tok/s")

    if fast:
        print(f"\n⚡⚡ FAST (50-100 tok/s):")
        for r in sorted(fast, key=lambda x: x['avg_throughput'], reverse=True):
            print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} tok/s")

    if standard:
        print(f"\n⚡ STANDARD (<50 tok/s):")
        for r in sorted(standard, key=lambda x: x['avg_throughput'], reverse=True):
            print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} tok/s")

    # Save results
    print("\n" + "="*70)
    output_file = 'small_models_benchmark.json'
    with open(output_file, 'w') as f:
        json.dump({
            'models': all_results,
            'total_time': total_time,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=2)

    print(f"💾 Results saved to: {output_file}")
    print(f"⏱️  Total benchmark time: {total_time:.1f}s")
    print("="*70)

    # Recommendations
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)

    if successful:
        print(f"\n🚀 For speed:        Use {fastest['name']}")
        print(f"💎 For value:        Use {best_value['name']}")
        print(f"📦 For minimum RAM:  Use {smallest['name']}")
        print(f"\n⚖️  Best balance:     Qwen 3B or DeepSeek 1.5B")
        print(f"🔬 For experiments:  Qwen 0.5B (ultra-fast testing)")

if __name__ == "__main__":
    main()
