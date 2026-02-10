# MLX AI Models Setup Guide for M4 Pro MacBook
## Hardware Specifications
- **Machine**: MacBook M4 Pro
- **Unified Memory**: 24GB
- **GPU Cores**: 16
- **CPU Cores**: 12
- **Purpose**: Security research class evaluation with uncensored/abliterated models

---

## Currently Installed Models (in /mlx directory)
✅ **Josiefied-Qwen3-14B-abliterated-v3-6bit** - 14B parameter, 6-bit quantization (~8-9GB)
✅ **Josiefied-Qwen3-1.7B-abliterated-v1-4bit** - 1.7B parameter, 4-bit quantization (~1GB)
✅ **WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx** - 7B coding-focused model (~4-5GB)

---

## Recommended Additional Uncensored/Abliterated Models for Your Hardware

### High Priority - Optimal for 24GB RAM

1. **mlx-community/Dolphin-Qwen2.5-7B-4bit**
   - Size: ~4-5GB
   - Strengths: Highly uncensored, excellent reasoning
   - Use case: General security testing, uncensored responses
   ```bash
   huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit --local-dir ./mlx/Dolphin-Qwen2.5-7B-4bit
   ```

2. **mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit**
   - Size: ~5GB
   - Strengths: Minimal guardrails, strong instruction following
   - Use case: Security research, penetration testing scenarios
   ```bash
   huggingface-cli download mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit --local-dir ./mlx/Hermes-3-Llama-3.1-8B-4bit
   ```

3. **mlx-community/Ministral-8B-Instruct-2410-4bit**
   - Size: ~5GB
   - Strengths: Fast inference, good for quick evaluations
   - Use case: Rapid testing of guardrail bypasses
   ```bash
   huggingface-cli download mlx-community/Ministral-8B-Instruct-2410-4bit --local-dir ./mlx/Ministral-8B-Instruct-2410-4bit
   ```

4. **mlx-community/Qwen2.5-14B-Instruct-4bit** (baseline for comparison)
   - Size: ~8GB
   - Strengths: Excellent performance, some guardrails (good for comparison)
   - Use case: Baseline to compare against abliterated versions
   ```bash
   huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit --local-dir ./mlx/Qwen2.5-14B-Instruct-4bit
   ```

5. **mlx-community/Llama-3.2-11B-Vision-Instruct-4bit**
   - Size: ~7GB
   - Strengths: Vision capabilities for image-based security testing
   - Use case: Testing multimodal vulnerabilities
   ```bash
   huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-4bit --local-dir ./mlx/Llama-3.2-11B-Vision-Instruct-4bit
   ```

### Medium Priority - Larger Models (will use more RAM)

6. **mlx-community/Qwen2.5-32B-Instruct-4bit**
   - Size: ~18-19GB
   - Strengths: Very capable, can run on your hardware but will use most RAM
   - Use case: Advanced reasoning tasks
   ```bash
   huggingface-cli download mlx-community/Qwen2.5-32B-Instruct-4bit --local-dir ./mlx/Qwen2.5-32B-Instruct-4bit
   ```

7. **mlx-community/DeepSeek-R1-Distill-Qwen-14B-4bit**
   - Size: ~8-9GB
   - Strengths: Reasoning-focused, recent model
   - Use case: Complex security analysis scenarios
   ```bash
   huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-14B-4bit --local-dir ./mlx/DeepSeek-R1-Distill-Qwen-14B-4bit
   ```

### Specialized Models

8. **mlx-community/CodeQwen1.5-7B-Chat-4bit**
   - Size: ~4GB
   - Strengths: Code generation, fewer content filters
   - Use case: Testing code generation vulnerabilities
   ```bash
   huggingface-cli download mlx-community/CodeQwen1.5-7B-Chat-4bit --local-dir ./mlx/CodeQwen1.5-7B-Chat-4bit
   ```

---

## Software Setup

### 1. Install MLX Framework
```bash
pip install mlx mlx-lm
```

### 2. Install Hugging Face CLI (for downloads)
```bash
pip install huggingface-hub
```

### 3. LM Studio with MLX Support

**LM Studio** natively supports MLX models on Apple Silicon:
- Download: https://lmstudio.ai/
- LM Studio automatically detects MLX-optimized models
- Uses Metal Performance Shaders for optimal GPU utilization

**Setup Steps:**
1. Download and install LM Studio
2. In LM Studio settings:
   - Enable "Metal" acceleration (should be default on M-series Macs)
   - Set context length to 4096-8192 (adjust based on model)
   - Enable "GPU offloading" to max
3. Point LM Studio to your `/mlx` directory as a custom model path

### 4. Alternative: MLX-LM (Command Line)

For maximum performance and control:
```bash
# Install MLX-LM
pip install mlx-lm

# Run a model directly
mlx_lm.generate --model ./mlx/Dolphin-Qwen2.5-7B-4bit --prompt "Your prompt here" --max-tokens 500
```

### 5. Python API Usage
```python
from mlx_lm import load, generate

model, tokenizer = load("./mlx/Dolphin-Qwen2.5-7B-4bit")
response = generate(model, tokenizer, prompt="Your security research prompt", max_tokens=500)
print(response)
```

---

## Performance Expectations on M4 Pro (24GB, 16 GPU)

| Model Size | Quantization | RAM Usage | Tokens/sec (est.) | Recommended Use |
|------------|--------------|-----------|-------------------|-----------------|
| 1.7B       | 4-bit        | ~1GB      | 80-120 tps        | Ultra-fast testing |
| 7B         | 4-bit        | ~4-5GB    | 40-60 tps         | Best balance |
| 8B         | 4-bit        | ~5GB      | 35-50 tps         | Excellent quality |
| 14B        | 4-bit        | ~8-9GB    | 20-30 tps         | High quality |
| 14B        | 6-bit        | ~10-11GB  | 15-25 tps         | Higher accuracy |
| 32B        | 4-bit        | ~18-19GB  | 8-15 tps          | Maximum capability |

---

## Download Script (All Recommended Models)

Create `download_models.sh`:
```bash
#!/bin/bash

# Ensure we're in the models directory
cd /Users/jonathanmallinger/models/mlx

# High priority models
huggingface-cli download mlx-community/Dolphin-Qwen2.5-7B-4bit --local-dir ./Dolphin-Qwen2.5-7B-4bit
huggingface-cli download mlx-community/NousResearch-Hermes-3-Llama-3.1-8B-4bit --local-dir ./Hermes-3-Llama-3.1-8B-4bit
huggingface-cli download mlx-community/Ministral-8B-Instruct-2410-4bit --local-dir ./Ministral-8B-Instruct-2410-4bit
huggingface-cli download mlx-community/Qwen2.5-14B-Instruct-4bit --local-dir ./Qwen2.5-14B-Instruct-4bit
huggingface-cli download mlx-community/Llama-3.2-11B-Vision-Instruct-4bit --local-dir ./Llama-3.2-11B-Vision-Instruct-4bit

# Medium priority (optional - larger models)
huggingface-cli download mlx-community/Qwen2.5-32B-Instruct-4bit --local-dir ./Qwen2.5-32B-Instruct-4bit
huggingface-cli download mlx-community/DeepSeek-R1-Distill-Qwen-14B-4bit --local-dir ./DeepSeek-R1-Distill-Qwen-14B-4bit

# Specialized
huggingface-cli download mlx-community/CodeQwen1.5-7B-Chat-4bit --local-dir ./CodeQwen1.5-7B-Chat-4bit

echo "Download complete!"
```

Run with:
```bash
chmod +x download_models.sh
./download_models.sh
```

---

## Finding More Abliterated/Uncensored Models

Search on Hugging Face:
```bash
# Search for MLX + abliterated models
huggingface-cli search mlx abliterated

# Search for MLX + uncensored
huggingface-cli search mlx uncensored

# Search for specific model families
huggingface-cli search "mlx-community/Dolphin"
huggingface-cli search "mlx-community/Hermes"
```

**Key Sources:**
- mlx-community organization: https://huggingface.co/mlx-community
- Look for tags: "abliterated", "uncensored", "no-guardrails"
- Model families: Dolphin, Hermes, WhiteRabbitNeo, Josiefied

---

## Best Practices for Security Research

1. **Multi-Model Testing**: Use 3-4 models with different architectures to evaluate guardrails
2. **Quantization Trade-offs**: 4-bit is best for your RAM; 6-bit if you need higher precision
3. **Benchmark Suite**: Test against standard jailbreak prompts to establish baseline
4. **Document Everything**: Keep logs of which models respond to which prompts

### Recommended Model Combination for Class:
- **Fast testing**: Josiefied-Qwen3-1.7B-abliterated-v1-4bit (already installed)
- **General use**: Dolphin-Qwen2.5-7B-4bit (download)
- **High quality**: Josiefied-Qwen3-14B-abliterated-v3-6bit (already installed)
- **Coding**: WhiteRabbitNeo or CodeQwen (mix of installed + download)
- **Baseline**: Qwen2.5-14B-Instruct-4bit (download for comparison)

---

## Troubleshooting

### If LM Studio doesn't detect MLX models:
1. Ensure models are in GGUF or MLX format
2. Check model directory has proper config files
3. Use "Add model from path" in LM Studio

### If inference is slow:
1. Close other memory-intensive applications
2. Use 4-bit quantization instead of 6-bit or 8-bit
3. Reduce context length in settings
4. Ensure GPU acceleration is enabled

### Memory issues:
- Monitor Activity Monitor during inference
- Start with 7B models, gradually test larger ones
- 32B models might cause memory pressure with large contexts

---

## Quick Start Command

After downloading, test a model immediately:
```bash
python3 -c "from mlx_lm import load, generate; model, tokenizer = load('./mlx/Dolphin-Qwen2.5-7B-4bit'); print(generate(model, tokenizer, prompt='Explain penetration testing', max_tokens=200))"
```

---

**Total Recommended Downloads**: ~50-60GB for all models
**Time estimate**: 1-3 hours depending on internet speed
**Optimal starter set**: Dolphin-7B, Hermes-8B, Qwen2.5-14B (~18GB total)
