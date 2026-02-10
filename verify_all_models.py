#!/usr/bin/env python3
"""
Comprehensive Model Verification Script
Tests all models to ensure they work properly
"""

import os
import time
import json
from pathlib import Path

def check_model_files(model_dir):
    """Check if model has all necessary files"""
    required_files = {
        'config': ['config.json'],
        'model': ['model.safetensors', 'weights.safetensors', 'pytorch_model.bin'],
        'tokenizer': ['tokenizer.json', 'tokenizer_config.json']
    }
    
    results = {}
    for category, possible_files in required_files.items():
        found = False
        for filename in possible_files:
            if (model_dir / filename).exists():
                found = True
                results[category] = filename
                break
        
        # Check for sharded files
        if not found and category == 'model':
            sharded = list(model_dir.glob('model-*-of-*.safetensors'))
            if sharded:
                found = True
                results[category] = f"{len(sharded)} sharded files"
        
        if not found:
            results[category] = None
    
    return results

def test_model_load(model_path):
    """Try to load model with MLX"""
    try:
        from mlx_lm import load
        print(f"  Loading model...")
        start = time.time()
        model, tokenizer = load(str(model_path))
        load_time = time.time() - start
        print(f"  ✓ Loaded in {load_time:.2f}s")
        return True, load_time
    except Exception as e:
        print(f"  ✗ Load failed: {e}")
        return False, 0

def test_model_generate(model_path):
    """Try to generate text with model"""
    try:
        from mlx_lm import load, generate
        
        model, tokenizer = load(str(model_path))
        
        print(f"  Testing generation...")
        start = time.time()
        response = generate(
            model, 
            tokenizer, 
            prompt="Test prompt: Say hello",
            max_tokens=20,
            verbose=False
        )
        gen_time = time.time() - start
        
        # Check if output is valid
        if len(response) > 0 and not all(ord(c) > 127 for c in response[:50]):
            tokens_est = len(response.split()) * 1.3
            tps = tokens_est / gen_time if gen_time > 0 else 0
            print(f"  ✓ Generated text: {len(response)} chars")
            print(f"  ✓ Speed: {tps:.1f} tokens/s")
            return True, tps, response[:100]
        else:
            print(f"  ✗ Invalid output (gibberish or empty)")
            return False, 0, response[:100]
            
    except Exception as e:
        print(f"  ✗ Generation failed: {e}")
        return False, 0, ""

def main():
    mlx_dir = Path("./mlx")
    
    print("="*70)
    print("🔍 COMPREHENSIVE MODEL VERIFICATION")
    print("="*70)
    print()
    
    models = sorted([d for d in mlx_dir.iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    results = {
        'working': [],
        'broken': [],
        'slow': [],
        'incomplete': []
    }
    
    for i, model_dir in enumerate(models, 1):
        model_name = model_dir.name
        print(f"\n[{i}/{len(models)}] Testing: {model_name}")
        print("-" * 70)
        
        # Check files
        files = check_model_files(model_dir)
        print(f"  Files: Config={files.get('config', '✗')} | "
              f"Model={files.get('model', '✗')} | "
              f"Tokenizer={files.get('tokenizer', '✗')}")
        
        # Check if all files present
        if None in files.values():
            print(f"  ⚠️  INCOMPLETE: Missing files")
            results['incomplete'].append({
                'name': model_name,
                'missing': [k for k, v in files.items() if v is None]
            })
            continue
        
        # Test loading
        can_load, load_time = test_model_load(model_dir)
        if not can_load:
            print(f"  ❌ BROKEN: Cannot load")
            results['broken'].append({
                'name': model_name,
                'reason': 'Load failed'
            })
            continue
        
        # Test generation
        can_generate, tps, sample = test_model_generate(model_dir)
        if not can_generate:
            print(f"  ❌ BROKEN: Generation failed or gibberish")
            results['broken'].append({
                'name': model_name,
                'reason': 'Generation failed',
                'sample': sample
            })
            continue
        
        # Classify by speed
        size_str = os.popen(f"du -sh '{model_dir}' | cut -f1").read().strip()
        if 'M' in size_str:
            size_gb = float(size_str.replace('M', '').replace(',', '.')) / 1024
        elif 'G' in size_str:
            size_gb = float(size_str.replace('G', '').replace(',', '.'))
        else:
            size_gb = 0.0
        
        model_info = {
            'name': model_name,
            'size': f"{size_gb:.1f}GB",
            'speed': f"{tps:.1f} t/s",
            'load_time': f"{load_time:.2f}s"
        }
        
        # Speed expectations based on size
        if size_gb < 2 and tps < 80:
            results['slow'].append(model_info)
            print(f"  ⚠️  SLOW: Expected 80+ t/s for {size_gb:.1f}GB model")
        elif 2 <= size_gb < 6 and tps < 40:
            results['slow'].append(model_info)
            print(f"  ⚠️  SLOW: Expected 40+ t/s for {size_gb:.1f}GB model")
        elif size_gb >= 6 and tps < 15:
            results['slow'].append(model_info)
            print(f"  ⚠️  SLOW: Expected 15+ t/s for {size_gb:.1f}GB model")
        else:
            results['working'].append(model_info)
            print(f"  ✅ WORKING PERFECTLY")
    
    # Summary
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)
    
    print(f"\n✅ WORKING MODELS ({len(results['working'])}):")
    for m in results['working']:
        print(f"  • {m['name']:<50} {m['size']:>8} @ {m['speed']:>12}")
    
    if results['slow']:
        print(f"\n⚠️  SLOW MODELS ({len(results['slow'])}):")
        for m in results['slow']:
            print(f"  • {m['name']:<50} {m['size']:>8} @ {m['speed']:>12}")
    
    if results['broken']:
        print(f"\n❌ BROKEN MODELS ({len(results['broken'])}):")
        for m in results['broken']:
            print(f"  • {m['name']:<50} Reason: {m['reason']}")
    
    if results['incomplete']:
        print(f"\n📦 INCOMPLETE MODELS ({len(results['incomplete'])}):")
        for m in results['incomplete']:
            print(f"  • {m['name']:<50} Missing: {', '.join(m['missing'])}")
    
    # Recommendations
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)
    
    if results['broken']:
        print("\n❌ Delete broken models:")
        for m in results['broken']:
            print(f"  rm -rf ./mlx/{m['name']}")
    
    if results['incomplete']:
        print("\n📦 Re-download incomplete models:")
        for m in results['incomplete']:
            print(f"  # Re-download: {m['name']}")
    
    print(f"\n✅ Keep these {len(results['working'])} working models!")
    
    # Save results
    with open('model_verification_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Full results saved to: model_verification_results.json")
    print()

if __name__ == "__main__":
    main()
