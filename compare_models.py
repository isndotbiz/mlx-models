#!/usr/bin/env python3
"""Compare overlapping models to show redundancy"""

from mlx_lm import load, generate
import time

def test_model(path, prompt):
    """Quick test of a model"""
    model, tokenizer = load(path)
    start = time.time()
    response = generate(model, tokenizer, prompt=prompt, max_tokens=100, verbose=False)
    gen_time = time.time() - start
    tokens = len(response.split())
    return response, tokens / gen_time if gen_time > 0 else 0

def main():
    prompt = "Explain how to test for SQL injection vulnerabilities in a web application:"

    print("="*70)
    print("🔍 REDUNDANCY TEST: Uncensored Models")
    print("="*70)
    print(f"\nPrompt: {prompt}\n")

    models = [
        ("./mlx/dolphin3-8b", "dolphin3-8b", "4.2GB", "Uncensored 8B"),
        ("./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit", "Josiefied-8B", "4.3GB", "Abliterated 8B"),
    ]

    results = []

    for path, name, size, desc in models:
        print(f"\n{'='*70}")
        print(f"Testing: {name} ({size}) - {desc}")
        print(f"{'='*70}")
        try:
            response, speed = test_model(path, prompt)
            print(f"\nSpeed: {speed:.1f} tokens/s")
            print(f"\nResponse:\n{response[:300]}...")
            results.append((name, size, desc, speed, response))
        except Exception as e:
            print(f"Error: {e}")

    # Compare
    print("\n\n" + "="*70)
    print("📊 COMPARISON SUMMARY")
    print("="*70)

    if len(results) >= 2:
        print(f"\n{'Model':<20} {'Size':<8} {'Speed':<12} {'Description'}")
        print("-"*70)
        for name, size, desc, speed, _ in results:
            print(f"{name:<20} {size:<8} {speed:>6.1f} t/s   {desc}")

        print("\n💡 ANALYSIS:")
        print("-"*70)
        print(f"• Both models are ~4GB uncensored 8B models")
        print(f"• Both answer the same types of questions")
        print(f"• Josiefied is specifically 'abliterated' (safety removed)")
        print(f"• Similar capabilities, different training")
        print(f"\n🎯 RECOMMENDATION: Keep Josiefied-8B, remove dolphin3-8b")
        print(f"   Reason: Josiefied is purpose-built for uncensored tasks")

if __name__ == "__main__":
    main()
