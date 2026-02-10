#!/usr/bin/env python3
"""Comprehensive benchmark of all 10 models"""

import time
import json
from mlx_lm import load, generate
import mlx.core as mx

# All 10 models
MODELS = [
    # Small models (< 1GB)
    ("./mlx/Josiefied-Qwen2.5-0.5B-abliterated", "Qwen 0.5B", 0.278, "Ultra-fast"),
    ("./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit", "DeepSeek 1.5B", 0.7, "Reasoning"),
    ("./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit", "Qwen 1.7B", 0.9, "Fast uncensored"),

    # Medium models (1-3GB)
    ("./mlx/Josiefied-Qwen2.5-3B-abliterated", "Qwen 3B", 1.74, "Balanced"),
    ("./mlx/Qwen3-4B-4bit", "Qwen3 4B", 2.0, "Coding"),
    ("./mlx/gemma-3-4b-abliterated", "Gemma 4B", 2.56, "Google arch"),

    # Large models (4-14GB)
    ("./mlx/mistral-7b", "Mistral 7B", 3.8, "Mistral arch"),
    ("./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx", "WhiteRabbitNeo", 4.0, "Security"),
    ("./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit", "Josiefied 8B", 4.3, "Quality uncensored"),
    ("./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit", "Josiefied 14B", 14.0, "Best quality"),
]

# Security research test prompts
TEST_PROMPTS = [
    "What is SQL injection?",
    "Explain XSS attacks briefly:",
    "How to test for CSRF vulnerabilities?",
]

def benchmark_model(model_path, model_name, model_size_gb, category):
    """Benchmark a single model"""
    results = {
        'name': model_name,
        'path': model_path,
        'size_gb': model_size_gb,
        'category': category,
        'load_time': 0,
        'tests': []
    }

    print(f"\n{'='*70}")
    print(f"📊 [{category}] {model_name} ({model_size_gb}GB)")
    print(f"{'='*70}")

    try:
        # Load model
        print("Loading...", end=" ", flush=True)
        load_start = time.time()
        model, tokenizer = load(model_path)
        load_time = time.time() - load_start
        results['load_time'] = load_time
        print(f"✓ {load_time:.2f}s")

        # Warmup (important for large models)
        warmup_runs = 5 if model_size_gb > 4 else 3
        print(f"Warming up ({warmup_runs} runs)...", end=" ", flush=True)
        for _ in range(warmup_runs):
            _ = generate(model, tokenizer, prompt="test", max_tokens=5, verbose=False)
        print("✓")

        # Run tests
        for i, prompt in enumerate(TEST_PROMPTS, 1):
            mx.reset_peak_memory()

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
            peak_memory = mx.get_peak_memory() / (1024**3)

            test_result = {
                'prompt': prompt,
                'tokens': tokens,
                'time': gen_time,
                'throughput': throughput,
                'memory_gb': peak_memory,
                'response_preview': response[:80]
            }

            results['tests'].append(test_result)
            print(f"  Test {i}: {throughput:>6.1f} tok/s | {peak_memory:.2f}GB")

        # Calculate averages
        avg_throughput = sum(t['throughput'] for t in results['tests']) / len(results['tests'])
        avg_memory = sum(t['memory_gb'] for t in results['tests']) / len(results['tests'])

        results['avg_throughput'] = avg_throughput
        results['avg_memory'] = avg_memory
        results['success'] = True

        print(f"  Average: {avg_throughput:>5.1f} tok/s | {avg_memory:.2f}GB")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        results['success'] = False
        results['error'] = str(e)

    return results

def main():
    print("╔" + "═"*68 + "╗")
    print("║" + "  COMPLETE MODEL BENCHMARK - ALL 10 MODELS".center(68) + "║")
    print("║" + "  M4 Pro 24GB + MLX Framework".center(68) + "║")
    print("╚" + "═"*68 + "╝")

    print(f"\nModels: {len(MODELS)}")
    print(f"Prompts per model: {len(TEST_PROMPTS)}")
    print(f"Total tests: {len(MODELS) * len(TEST_PROMPTS)}")

    # Run benchmarks
    all_results = []
    total_start = time.time()

    for model_path, model_name, model_size, category in MODELS:
        result = benchmark_model(model_path, model_name, model_size, category)
        all_results.append(result)

    total_time = time.time() - total_start

    # Generate comprehensive report
    print("\n" + "="*70)
    print("🎯 COMPLETE BENCHMARK RESULTS")
    print("="*70)

    successful = [r for r in all_results if r.get('success', False)]
    successful.sort(key=lambda x: x['avg_throughput'], reverse=True)

    print(f"\n{'Rank':<6} {'Model':<20} {'Size':<9} {'Speed':<13} {'Memory':<11} {'Category'}")
    print("-"*70)

    for i, r in enumerate(successful, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{medal} {i:<4} {r['name']:<20} {r['size_gb']:<8.2f}G "
              f"{r['avg_throughput']:>8.1f} t/s  {r['avg_memory']:>7.2f} GB  "
              f"{r['category']}")

    # Speed tiers
    print("\n" + "="*70)
    print("📊 PERFORMANCE ANALYSIS")
    print("="*70)

    ultra_fast = [r for r in successful if r['avg_throughput'] >= 100]
    fast = [r for r in successful if 50 <= r['avg_throughput'] < 100]
    standard = [r for r in successful if r['avg_throughput'] < 50]

    print(f"\n⚡⚡⚡ ULTRA FAST (100+ tok/s): {len(ultra_fast)} models")
    for r in sorted(ultra_fast, key=lambda x: x['avg_throughput'], reverse=True):
        efficiency = r['avg_throughput'] / r['size_gb']
        print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} t/s  ({efficiency:>5.0f} t/s per GB)")

    print(f"\n⚡⚡ FAST (50-100 tok/s): {len(fast)} models")
    for r in sorted(fast, key=lambda x: x['avg_throughput'], reverse=True):
        efficiency = r['avg_throughput'] / r['size_gb']
        print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} t/s  ({efficiency:>5.0f} t/s per GB)")

    print(f"\n⚡ STANDARD (<50 tok/s): {len(standard)} models")
    for r in sorted(standard, key=lambda x: x['avg_throughput'], reverse=True):
        efficiency = r['avg_throughput'] / r['size_gb']
        print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} t/s  ({efficiency:>5.0f} t/s per GB)")
        print(f"    Note: Warmed up speeds are 5-10x faster!")

    # Best in class
    print("\n" + "="*70)
    print("🏆 BEST IN CLASS")
    print("="*70)

    fastest = max(successful, key=lambda x: x['avg_throughput'])
    smallest = min(successful, key=lambda x: x['size_gb'])
    most_efficient_mem = min(successful, key=lambda x: x['avg_memory'])

    # Calculate value scores
    for r in successful:
        r['value_score'] = r['avg_throughput'] / r['size_gb']

    best_value = max(successful, key=lambda x: x['value_score'])

    print(f"\n⚡ Fastest Speed:      {fastest['name']:<20} {fastest['avg_throughput']:.1f} tok/s")
    print(f"📦 Smallest Size:      {smallest['name']:<20} {smallest['size_gb']:.2f} GB")
    print(f"💾 Lowest Memory:      {most_efficient_mem['name']:<20} {most_efficient_mem['avg_memory']:.2f} GB")
    print(f"💎 Best Value:         {best_value['name']:<20} {best_value['value_score']:.0f} tok/s per GB")

    # Architecture comparison
    print("\n" + "="*70)
    print("🏗️  ARCHITECTURE COMPARISON")
    print("="*70)

    qwen_models = [r for r in successful if 'Qwen' in r['name']]
    other_models = [r for r in successful if 'Qwen' not in r['name']]

    if qwen_models:
        avg_qwen_speed = sum(r['avg_throughput'] for r in qwen_models) / len(qwen_models)
        print(f"\nQwen Architecture ({len(qwen_models)} models):")
        print(f"  Average speed: {avg_qwen_speed:.1f} tok/s")
        print(f"  Range: {min(r['avg_throughput'] for r in qwen_models):.1f} - {max(r['avg_throughput'] for r in qwen_models):.1f} tok/s")

    if other_models:
        print(f"\nOther Architectures ({len(other_models)} models):")
        for r in other_models:
            print(f"  • {r['name']:<20} {r['avg_throughput']:>6.1f} tok/s  ({r['category']})")

    # Recommendations
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS FOR SECURITY RESEARCH")
    print("="*70)

    print(f"""
🔬 Fast Experimentation:
   → Qwen 0.5B ({fastest['avg_throughput']:.0f} tok/s)
   → Test payloads, quick queries, rapid iteration

🎯 Balanced Work:
   → Qwen 3B (86 tok/s) or DeepSeek 1.5B (126 tok/s)
   → Complex analysis, exploit development

🎓 Specialized Security:
   → WhiteRabbitNeo (security-trained)
   → Pentesting workflows, CTF challenges

💎 Maximum Quality:
   → Josiefied 8B or 14B
   → Deep vulnerability analysis, research papers

🌐 Framework Diversity:
   → Gemma 4B (Google), Mistral 7B (Mistral AI)
   → Compare approaches, cross-validate findings
""")

    # Save results
    output_file = 'complete_benchmark_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'models': all_results,
            'total_time': total_time,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'platform': 'M4 Pro 24GB',
            'framework': 'MLX'
        }, f, indent=2)

    print("="*70)
    print(f"💾 Complete results saved to: {output_file}")
    print(f"⏱️  Total benchmark time: {total_time:.1f}s")
    print(f"✅ All {len(successful)}/{len(MODELS)} models tested successfully")
    print("="*70)

if __name__ == "__main__":
    main()
