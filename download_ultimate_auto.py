#!/usr/bin/env python3
"""
Ultimate Pack Downloader - Automatic (No prompts)
Downloads 7 essential models without user interaction
"""

from huggingface_hub import snapshot_download
import os
from pathlib import Path
import time

models = [
    ("Josiefied-Qwen3-8B-abliterated-v1-4bit", "mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit", "5GB", "Uncensored"),
    ("Llama-3.2-11B-Vision-abliterated-4bit", "mlx-community/Llama-3.2-11B-Vision-Instruct-abliterated-4-bit", "7GB", "Vision"),
    ("DeepSeek-R1-Distill-Qwen-7B", "mlx-community/DeepSeek-R1-Distill-Qwen-7B", "5GB", "Reasoning"),
    ("DeepSeek-R1-Distill-Qwen-1.5B-3bit", "mlx-community/DeepSeek-R1-Distill-Qwen-1.5B-3bit", "1GB", "Fast Reasoning"),
    ("Qwen3-Coder-7B-4bit", "Qwen/Qwen3-Coder-7B-4bit-MLX", "5GB", "Coding"),
    ("deepseek-coder-1.3b-base", "mlx-community/deepseek-coder-1.3b-base-mlx", "1GB", "Fast Coding"),
    ("Qwen3-4B-4bit", "Qwen/Qwen3-4B-MLX-4bit", "2.5GB", "General"),
]

print("="*60)
print("🏆 ULTIMATE PACK DOWNLOADER (AUTOMATIC)")
print("="*60)
print(f"\nDownloading 7 models (~31GB total)")
print(f"Estimated time: 1-3 hours depending on internet speed")
print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60 + "\n")

Path("./mlx").mkdir(exist_ok=True)

successful = 0
failed = 0
start_time = time.time()

for i, (name, repo, size, category) in enumerate(models, 1):
    local_dir = f"./mlx/{name}"
    
    if os.path.exists(local_dir):
        print(f"[{i}/{len(models)}] ⊘ {name} already exists, skipping\n")
        successful += 1
        continue
    
    print(f"[{i}/{len(models)}] Downloading {name} ({size}, {category})")
    print(f"  From: {repo}")
    
    model_start = time.time()
    try:
        snapshot_download(
            repo_id=repo,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        elapsed = time.time() - model_start
        print(f"  ✓ Complete in {elapsed/60:.1f} minutes\n")
        successful += 1
    except Exception as e:
        print(f"  ✗ Error: {e}\n")
        failed += 1

total_time = time.time() - start_time

print("="*60)
print("🎉 DOWNLOAD COMPLETE!")
print("="*60)
print(f"\nTotal time: {total_time/60:.1f} minutes ({total_time/3600:.1f} hours)")
print(f"✓ Successful: {successful} models")
if failed > 0:
    print(f"✗ Failed: {failed} models")

print("\n📊 Your complete model collection:")
print("  ✓ Josiefied-Qwen3-1.7B (already had)")
print("  ✓ Josiefied-Qwen3-8B (NEW) - Balanced uncensored")
print("  ✓ Llama-3.2-11B-Vision (NEW) - Multimodal!")
print("  ✓ DeepSeek-R1-7B (NEW) - Reasoning")
print("  ✓ DeepSeek-R1-1.5B (NEW) - Fast reasoning")
print("  ✓ Qwen3-Coder-7B (NEW) - Coding")
print("  ✓ deepseek-coder-1.3b (NEW) - Fast coding")
print("  ✓ Qwen3-4B (NEW) - Daily driver")

print("\n🚀 Next steps:")
print("  python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit")
print("  ./test_optimization.sh")
print("  open '/Applications/LM Studio.app'")
print("")
