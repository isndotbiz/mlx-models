#!/usr/bin/env python3
"""
Ultimate Pack Downloader
Downloads best models across all categories
"""

from huggingface_hub import snapshot_download
import os
from pathlib import Path

# Model list for ultimate pack
models = [
    {
        "name": "Josiefied-Qwen3-8B-abliterated-v1-4bit",
        "repo": "mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit",
        "size": "5GB",
        "category": "Uncensored",
        "priority": 1
    },
    {
        "name": "Llama-3.2-11B-Vision-abliterated-4bit",
        "repo": "mlx-community/Llama-3.2-11B-Vision-Instruct-abliterated-4-bit",
        "size": "7GB",
        "category": "Vision (Uncensored)",
        "priority": 2
    },
    {
        "name": "DeepSeek-R1-Distill-Qwen-7B",
        "repo": "mlx-community/DeepSeek-R1-Distill-Qwen-7B",
        "size": "5GB",
        "category": "Reasoning",
        "priority": 1
    },
    {
        "name": "DeepSeek-R1-Distill-Qwen-1.5B-3bit",
        "repo": "mlx-community/DeepSeek-R1-Distill-Qwen-1.5B-3bit",
        "size": "1GB",
        "category": "Fast Reasoning",
        "priority": 1
    },
    {
        "name": "Qwen3-Coder-7B-4bit",
        "repo": "Qwen/Qwen3-Coder-7B-4bit-MLX",
        "size": "5GB",
        "category": "Coding",
        "priority": 1
    },
    {
        "name": "deepseek-coder-1.3b-base",
        "repo": "mlx-community/deepseek-coder-1.3b-base-mlx",
        "size": "1GB",
        "category": "Fast Coding",
        "priority": 1
    },
    {
        "name": "Qwen3-4B-4bit",
        "repo": "Qwen/Qwen3-4B-MLX-4bit",
        "size": "2.5GB",
        "category": "General",
        "priority": 1
    },
]

optional_model = {
    "name": "DeepSeek-R1-Distill-Qwen-32B-4bit",
    "repo": "mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit",
    "size": "19GB",
    "category": "Maximum Quality",
    "priority": 3
}

def download_model(model_info, base_dir="./mlx"):
    """Download a single model"""
    local_dir = os.path.join(base_dir, model_info["name"])
    
    # Skip if already exists
    if os.path.exists(local_dir):
        print(f"⊘ {model_info['name']} already exists, skipping")
        return True
    
    print(f"\n{'='*60}")
    print(f"Downloading: {model_info['name']}")
    print(f"Category: {model_info['category']}")
    print(f"Size: {model_info['size']}")
    print(f"From: {model_info['repo']}")
    print(f"{'='*60}\n")
    
    try:
        snapshot_download(
            repo_id=model_info["repo"],
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        print(f"\n✓ {model_info['name']} downloaded successfully!\n")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading {model_info['name']}: {e}\n")
        return False

def main():
    print("="*60)
    print("🏆 ULTIMATE MODEL PACK DOWNLOADER")
    print("="*60)
    print("\nThis will download 7 essential models (~31GB):")
    print("\nUNCENSORED:")
    print("  • Josiefied-Qwen3-8B-abliterated (5GB)")
    print("  • Llama-3.2-11B-Vision-abliterated (7GB)")
    print("\nREASONING:")
    print("  • DeepSeek-R1-Distill-Qwen-7B (5GB)")
    print("  • DeepSeek-R1-1.5B-3bit (1GB)")
    print("\nCODING:")
    print("  • Qwen3-Coder-7B-4bit (5GB)")
    print("  • deepseek-coder-1.3b (1GB)")
    print("\nGENERAL:")
    print("  • Qwen3-4B-4bit (2.5GB)")
    print("\n" + "="*60)
    
    # Create mlx directory if it doesn't exist
    Path("./mlx").mkdir(exist_ok=True)
    
    # Download all models
    successful = 0
    failed = 0
    
    for i, model in enumerate(models, 1):
        print(f"\n[{i}/{len(models)}] Starting download...")
        if download_model(model):
            successful += 1
        else:
            failed += 1
    
    # Ask about optional 32B model
    print("\n" + "="*60)
    print("OPTIONAL: DeepSeek-R1-32B-4bit (19GB)")
    print("Near GPT-4 quality reasoning")
    print("Warning: Uses most of your 24GB RAM")
    print("="*60)
    
    response = input("\nDownload 32B model? (y/N): ").strip().lower()
    if response == 'y':
        print("\n[8/8] Downloading optional powerhouse...")
        if download_model(optional_model):
            successful += 1
        else:
            failed += 1
    else:
        print("\n⊘ Skipping 32B model")
    
    # Summary
    print("\n" + "="*60)
    print("🎉 DOWNLOAD COMPLETE!")
    print("="*60)
    print(f"\n✓ Successfully downloaded: {successful} models")
    if failed > 0:
        print(f"✗ Failed: {failed} models")
    
    print("\nYour models are in: ./mlx/")
    print("\nNext steps:")
    print("  1. Test a model:")
    print("     python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit")
    print("\n  2. Run optimization test:")
    print("     ./test_optimization.sh")
    print("\n  3. Open LM Studio:")
    print("     open '/Applications/LM Studio.app'")
    print("     Set engine to: MLX (Apple Silicon GPU)")
    print("")

if __name__ == "__main__":
    main()
