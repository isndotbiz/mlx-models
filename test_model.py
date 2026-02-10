#!/usr/bin/env .venv/bin/python3
"""
Quick test script for MLX models
Usage: python3 test_model.py [model_path]
Example: python3 test_model.py ./mlx/Dolphin-Qwen2.5-7B-4bit
"""

import sys
import time
from pathlib import Path

try:
    from mlx_lm import load, generate
except ImportError:
    print("ERROR: mlx_lm not installed!")
    print("Install with: pip install mlx mlx-lm")
    sys.exit(1)

def test_model(model_path):
    """Test a model with a simple prompt"""
    
    print(f"\n{'='*60}")
    print(f"Testing Model: {model_path}")
    print(f"{'='*60}\n")
    
    # Check if path exists
    if not Path(model_path).exists():
        print(f"ERROR: Model path does not exist: {model_path}")
        return
    
    # Load model
    print("Loading model...")
    start_time = time.time()
    try:
        model, tokenizer = load(model_path)
        load_time = time.time() - start_time
        print(f"✓ Model loaded in {load_time:.2f} seconds\n")
    except Exception as e:
        print(f"ERROR loading model: {e}")
        return
    
    # Test prompts for security research evaluation
    test_prompts = [
        {
            "name": "Basic Response Test",
            "prompt": "Explain what penetration testing is in one paragraph."
        },
        {
            "name": "Uncensored Test",
            "prompt": "List common security vulnerabilities in web applications."
        },
        {
            "name": "Code Generation Test",
            "prompt": "Write a Python function to check if a password is strong."
        }
    ]
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\n--- Test {i}/{len(test_prompts)}: {test['name']} ---")
        print(f"Prompt: {test['prompt']}\n")
        
        start_time = time.time()
        try:
            response = generate(
                model, 
                tokenizer, 
                prompt=test['prompt'],
                max_tokens=200,
                verbose=False
            )
            gen_time = time.time() - start_time
            
            # Calculate tokens per second (rough estimate)
            # Assuming average token is ~4 characters
            estimated_tokens = len(response) // 4
            tps = estimated_tokens / gen_time if gen_time > 0 else 0
            
            print(f"Response:\n{response}\n")
            print(f"Generation time: {gen_time:.2f}s")
            print(f"Estimated speed: {tps:.1f} tokens/second")
            
        except Exception as e:
            print(f"ERROR during generation: {e}")
    
    print(f"\n{'='*60}")
    print("Test complete!")
    print(f"{'='*60}\n")

def list_available_models():
    """List all available MLX models in the mlx directory"""
    mlx_dir = Path("./mlx")
    if not mlx_dir.exists():
        print("No ./mlx directory found")
        return []
    
    models = [d for d in mlx_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    return models

if __name__ == "__main__":
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
        test_model(model_path)
    else:
        print("MLX Model Tester")
        print("="*60)
        print("\nAvailable models in ./mlx/:\n")
        
        models = list_available_models()
        if models:
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model.name}")
            
            print("\nUsage:")
            print(f"  python3 test_model.py ./mlx/MODEL_NAME")
            print("\nExample:")
            print(f"  python3 test_model.py ./mlx/{models[0].name}")
        else:
            print("  No models found!")
            print("\nRun ./download_models.sh to download models first.")
        print()
