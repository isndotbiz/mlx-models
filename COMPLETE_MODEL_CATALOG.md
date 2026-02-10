# Complete MLX Model Catalog for M4 Pro (24GB RAM)
### Updated February 2026

## 🎯 Quick Navigation
- [Uncensored/Abliterated Models](#uncensored) - For security research
- [Reasoning Models](#reasoning) - DeepSeek R1, QwQ
- [Coding Models](#coding) - Qwen3-Coder, DeepSeek-Coder
- [Vision Models](#vision) - Multimodal capabilities
- [Latest Models](#latest) - Qwen3, Llama 3.2, Gemma 3
- [Performance Table](#performance) - Speed estimates

---

## <a name="uncensored"></a>🔓 Uncensored/Abliterated Models

### Josiefied Series (31 models available!)

#### High Priority - Verified Working

**Josiefied-Qwen3-8B-abliterated-v1-4bit**
```bash
huggingface-cli download mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --local-dir ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit
```
- Size: 4.5 GB | Speed: 50-65 t/s | **RECOMMENDED**
- Use: General uncensored, balanced performance

**Josiefied-Qwen3-14B-abliterated-v3-4bit**
```bash
huggingface-cli download mlx-community/Josiefied-Qwen3-14B-abliterated-v3-4bit \
  --local-dir ./mlx/Josiefied-Qwen3-14B-abliterated-v3-4bit
```
- Size: 8 GB | Speed: 35-45 t/s
- Use: High-quality uncensored responses

**Josiefied-Qwen3-4B-abliterated-v1-4bit**
```bash
huggingface-cli download mlx-community/Josiefied-Qwen3-4B-abliterated-v1-4bit \
  --local-dir ./mlx/Josiefied-Qwen3-4B-abliterated-v1-4bit
```
- Size: 2.5 GB | Speed: 80-100 t/s | **FASTEST**
- Use: Ultra-fast uncensored testing

**Josiefied-DeepSeek-R1-0528-Qwen3-8B-abliterated-v1-4bit**
```bash
huggingface-cli download mlx-community/Josiefied-DeepSeek-R1-0528-Qwen3-8B-abliterated-v1-4bit \
  --local-dir ./mlx/Josiefied-DeepSeek-R1-0528-Qwen3-8B-abliterated-v1-4bit
```
- Size: 5 GB | Speed: 50-60 t/s
- Use: Uncensored reasoning tasks

### Other Abliterated Models

**Meta-Llama-3.1-8B-Instruct-abliterated-8bit**
```bash
huggingface-cli download mlx-community/Meta-Llama-3.1-8B-Instruct-abliterated-8bit \
  --local-dir ./mlx/Meta-Llama-3.1-8B-Instruct-abliterated-8bit
```
- Size: 8 GB | Speed: 45-55 t/s
- Use: High-quality abliterated Llama

**Dark-Champion-MOE-21B-Q6** (MoE!)
```bash
huggingface-cli download mlx-community/Llama-3.2-8X4B-MOE-V2-Dark-Champion-Instruct-uncensored-abliterated-21B-Q_6-MLX \
  --local-dir ./mlx/Dark-Champion-MOE-21B-Q6
```
- Size: 14 GB | Speed: 30-40 t/s
- Use: Uncensored Mixture of Experts

**Llama-3.2-11B-Vision-Instruct-abliterated-4bit**
```bash
huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-abliterated-4-bit \
  --local-dir ./mlx/Llama-3.2-11B-Vision-abliterated-4bit
```
- Size: 6-7 GB | Speed: 40-50 t/s
- Use: Uncensored vision model!

---

## <a name="reasoning"></a>🧠 Reasoning Models

### DeepSeek R1 Series (January 2025 release)

**DeepSeek-R1-Distill-Qwen-7B** ⭐ BEST BALANCE
```bash
huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-7B \
  --local-dir ./mlx/DeepSeek-R1-Distill-Qwen-7B
```
- Size: 4-5 GB | Speed: 55-65 t/s
- Use: Efficient reasoning

**DeepSeek-R1-Distill-Qwen-32B-4bit** ⭐ HIGHEST QUALITY
```bash
huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-32B-4bit \
  --local-dir ./mlx/DeepSeek-R1-Distill-Qwen-32B-4bit
```
- Size: 18-20 GB | Speed: 20-30 t/s
- Use: Near GPT-4 level reasoning

**DeepSeek-R1-Distill-Qwen-1.5B-3bit** ⚡ FASTEST
```bash
huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-1.5B-3bit \
  --local-dir ./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit
```
- Size: 0.8-1 GB | Speed: 120+ t/s
- Use: Ultra-fast reasoning

**DeepSeek-R1-0528-Qwen3-8B-8bit**
```bash
huggingface-cli download mlx-community/DeepSeek-R1-0528-Qwen3-8B-8bit \
  --local-dir ./mlx/DeepSeek-R1-0528-Qwen3-8B-8bit
```
- Size: 8 GB | Speed: 50-60 t/s
- Use: Higher quality reasoning

### QwQ Series

**QwQ-32B-4bit**
```bash
huggingface-cli download lmstudio-community/QwQ-32B-MLX-4bit \
  --local-dir ./mlx/QwQ-32B-4bit
```
- Size: 18-20 GB | Speed: 20-30 t/s
- Use: Apache 2 licensed, 128K context

---

## <a name="coding"></a>💻 Coding Models

### Qwen3-Coder Series

**Qwen3-Coder-7B-4bit** ⭐ RECOMMENDED
```bash
huggingface-cli download Qwen/Qwen3-Coder-7B-4bit-MLX \
  --local-dir ./mlx/Qwen3-Coder-7B-4bit
```
- Size: 4-5 GB | Speed: 55-65 t/s
- Use: Fast coding assistance

**Qwen3-Coder-30B-4bit**
```bash
huggingface-cli download Qwen/Qwen3-Coder-30B-4bit-MLX \
  --local-dir ./mlx/Qwen3-Coder-30B-4bit
```
- Size: 17.2 GB | Speed: 22-28 t/s
- Use: Advanced coding

### DeepSeek-Coder

**deepseek-coder-1.3b-base** ⚡ FASTEST
```bash
huggingface-cli download mlx-community/deepseek-coder-1.3b-base-mlx \
  --local-dir ./mlx/deepseek-coder-1.3b-base
```
- Size: 1 GB | Speed: 100+ t/s
- Use: Ultra-fast code completion

---

## <a name="vision"></a>👁️ Vision Models (Multimodal)

**Llama-3.2-11B-Vision-abliterated** ⭐ UNCENSORED VISION
```bash
huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-abliterated-4-bit \
  --local-dir ./mlx/Llama-3.2-11B-Vision-abliterated-4bit
```
- Size: 6-7 GB | Speed: 40-50 t/s
- Use: Uncensored multimodal!

**Qwen2.5-VL-32B** (requires mlx-vlm)
- Size: 18-22 GB | Speed: 20-28 t/s
- Use: GPT-4-class vision

**Qwen3-VL** (Latest!)
- Available in 3B, 7B sizes
- Strongest multimodal reasoning

---

## <a name="latest"></a>🆕 Latest Models

### Qwen3 Series (2025-2026)

**Qwen3-4B-4bit** ⭐ DAILY DRIVER
```bash
huggingface-cli download Qwen/Qwen3-4B-MLX-4bit \
  --local-dir ./mlx/Qwen3-4B-4bit
```
- Size: 2.5 GB | Speed: 70-90 t/s
- Use: Fast general-purpose

**Qwen3-0.6B-4bit** ⚡ ULTRA-FAST
```bash
huggingface-cli download Qwen/Qwen3-0.6B-MLX-4bit \
  --local-dir ./mlx/Qwen3-0.6B-4bit
```
- Size: 0.4-0.5 GB | Speed: 150+ t/s
- Use: Edge deployment, rapid testing

### Llama 3.2 Series

**Llama-3.2-3B-Instruct-4bit**
```bash
huggingface-cli download mlx-community/Llama-3.2-3B-Instruct-4bit \
  --local-dir ./mlx/Llama-3.2-3B-Instruct-4bit
```
- Size: 1.8-2 GB | Speed: 80-100 t/s
- Use: Fast general-purpose

**Llama-3.2-1B-Instruct-4bit**
```bash
huggingface-cli download mlx-community/Llama-3.2-1B-Instruct-4bit \
  --local-dir ./mlx/Llama-3.2-1B-Instruct-4bit
```
- Size: 0.7-0.8 GB | Speed: 120+ t/s
- Use: Ultra-fast

### Gemma 3 Series

**Gemma-3-4b-pt-4bit**
```bash
huggingface-cli download mlx-community/gemma-3-4b-pt-4bit \
  --local-dir ./mlx/gemma-3-4b-pt-4bit
```
- Size: 2.5 GB | Speed: 70-90 t/s
- Use: Google's efficient model

### Phi-4

**Phi-4-4bit**
```bash
huggingface-cli download mlx-community/phi-4-4bit \
  --local-dir ./mlx/phi-4-4bit
```
- Size: 7.7 GB | Speed: 35-45 t/s
- Use: Microsoft's reasoning model

---

## <a name="performance"></a>📊 Performance Table (M4 Pro 24GB)

| Model | Size | Params | Speed | RAM Usage | Best For |
|-------|------|--------|-------|-----------|----------|
| Qwen3-0.6B | 0.5GB | 0.6B | 150+ t/s | 1GB | Ultra-fast |
| DeepSeek-Coder-1.3B | 1GB | 1.3B | 100+ t/s | 1.5GB | Fast coding |
| DeepSeek-R1-1.5B | 1GB | 1.5B | 120+ t/s | 1.5GB | Fast reasoning |
| Llama-3.2-1B | 0.8GB | 1B | 120+ t/s | 1.2GB | Fast chat |
| Qwen3-4B | 2.5GB | 4B | 70-90 t/s | 3GB | Daily driver |
| Josiefied-Qwen3-4B | 2.5GB | 4B | 80-100 t/s | 3GB | Fast uncensored |
| Qwen3-Coder-7B | 4.5GB | 7B | 55-65 t/s | 5GB | Coding |
| DeepSeek-R1-7B | 4.5GB | 7B | 55-65 t/s | 5GB | Reasoning |
| Llama-3.2-Vision-11B | 7GB | 11B | 40-50 t/s | 8GB | Vision |
| Josiefied-Qwen3-8B | 4.5GB | 8B | 50-65 t/s | 5GB | Uncensored ⭐ |
| Llama-3.1-8B-abliterated | 8GB | 8B | 45-55 t/s | 9GB | High-quality |
| Josiefied-Qwen3-14B | 8GB | 14B | 35-45 t/s | 10GB | Premium |
| Dark-Champion-MOE-21B | 14GB | 21B | 30-40 t/s | 15GB | MoE |
| DeepSeek-R1-32B | 19GB | 32B | 20-30 t/s | 20GB | Max quality |
| Qwen3-Coder-30B | 17GB | 30B | 22-28 t/s | 19GB | Max coding |

---

## 🎯 Recommended Starter Pack

**For Security Research (Your Use Case):**

1. **Ultra-fast testing:**
   - Josiefied-Qwen3-1.7B-abliterated (already installed) ✓
   - DeepSeek-R1-1.5B-3bit (NEW)

2. **Balanced performance:**
   - Josiefied-Qwen3-8B-abliterated-v1-4bit ⭐
   - DeepSeek-R1-Distill-Qwen-7B

3. **High quality:**
   - Josiefied-Qwen3-14B-abliterated-v3-4bit
   - DeepSeek-R1-32B-4bit

4. **Specialized:**
   - Qwen3-Coder-7B-4bit (coding)
   - Llama-3.2-11B-Vision-abliterated (vision)

**Total: ~45GB for complete set**

---

## 🔍 Finding More Models

### Search Commands:
```bash
# Search for abliterated models
huggingface-cli search mlx abliterated

# Search for Josiefied models
huggingface-cli search "mlx-community/Josiefied"

# Browse collections
# Visit: https://huggingface.co/collections/mlx-community/josiefied-and-abliterated-models
```

### Browse Online:
- https://huggingface.co/mlx-community
- https://huggingface.co/lmstudio-community
- Filter by "mlx", "4bit", "abliterated"

---

## 💡 Pro Tips

1. **Start small**: Test 4B-8B models first
2. **4-bit is optimal**: Best balance for M4 Pro
3. **Leave 6GB free**: For system + context
4. **Use MLX engine**: 20-50% faster than llama.cpp
5. **Enable Flash Attention**: For long contexts
6. **Cache models locally**: Faster loading

---

*Last updated: February 2026 | 80+ MLX models cataloged*
