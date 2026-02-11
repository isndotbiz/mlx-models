#!/usr/bin/env python3
"""
Direct MLX benchmark for comparison with server-based approaches
"""

import time
import json
from mlx_lm import load, generate
import mlx.core as mx

MODEL_PATH = "./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit"

SECURITY_PROMPT = "Explain a buffer overflow attack and provide a C code example"

TEST_PROMPTS = [
    "What is SQL injection and how does it work?",
    "Explain cross-site scripting (XSS) attacks",
    "How do you test for CSRF vulnerabilities?",
    SECURITY_PROMPT
]

def benchmark_direct_mlx():
    """Benchmark direct MLX-LM usage"""
    print("="*70)
    print("📊 Direct MLX-LM Benchmark")
    print(f"Model: {MODEL_PATH}")
    print("="*70)

    results = {
        "method": "Direct MLX-LM",
        "model_path": MODEL_PATH,
        "tests": []
    }

    # Load model
    print("\nLoading model...", end=" ", flush=True)
    load_start = time.time()
    model, tokenizer = load(MODEL_PATH)
    load_time = time.time() - load_start
    results["load_time"] = load_time
    print(f"✓ {load_time:.2f}s")

    # Warmup
    print("Warming up...", end=" ", flush=True)
    for _ in range(3):
        _ = generate(model, tokenizer, prompt="test", max_tokens=10, verbose=False)
    print("✓")

    # Run tests
    print("\nRunning tests:")
    for i, prompt in enumerate(TEST_PROMPTS, 1):
        print(f"\n  Test {i}/{len(TEST_PROMPTS)}: {prompt[:50]}...")

        try:
            mx.metal.reset_peak_memory()

            start = time.time()
            response = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=200,
                verbose=False
            )
            gen_time = time.time() - start

            # Calculate metrics
            tokens = len(tokenizer.encode(response))
            throughput = tokens / gen_time if gen_time > 0 else 0
            peak_memory = mx.metal.get_peak_memory() / (1024**3)

            test_result = {
                "prompt": prompt,
                "tokens": tokens,
                "time": gen_time,
                "tokens_per_second": throughput,
                "memory_gb": peak_memory,
                "response": response,
                "response_preview": response[:200],
                "success": True
            }

            results["tests"].append(test_result)
            print(f"    ✓ {throughput:.1f} tok/s | {peak_memory:.2f}GB | {tokens} tokens")
            print(f"    Preview: {response[:100]}...")

        except Exception as e:
            print(f"    ✗ Error: {e}")
            results["tests"].append({
                "prompt": prompt,
                "success": False,
                "error": str(e)
            })

    # Calculate averages
    successful = [t for t in results["tests"] if t["success"]]
    if successful:
        results["avg_tokens_per_second"] = sum(t["tokens_per_second"] for t in successful) / len(successful)
        results["avg_memory_gb"] = sum(t["memory_gb"] for t in successful) / len(successful)
        results["avg_time"] = sum(t["time"] for t in successful) / len(successful)

    # Print summary
    print("\n" + "="*70)
    print("📈 SUMMARY")
    print("="*70)
    if successful:
        print(f"Successful tests: {len(successful)}/{len(TEST_PROMPTS)}")
        print(f"Average speed: {results['avg_tokens_per_second']:.1f} tok/s")
        print(f"Average memory: {results['avg_memory_gb']:.2f} GB")
        print(f"Load time: {results['load_time']:.2f}s")
    else:
        print("No successful tests")

    # Save results
    output_file = 'direct_mlx_benchmark.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")

    return results


if __name__ == "__main__":
    benchmark_direct_mlx()
