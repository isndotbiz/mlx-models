# LM Studio Optimization Guide for M4 Pro (24GB)

## 🚀 Critical Optimization: USE MLX ENGINE!

### **MOST IMPORTANT SETTING:**

**MLX is 20-50% FASTER than llama.cpp on M4 Pro!**

Recent benchmarks:
- MLX: **~83 tokens/s** generation
- llama.cpp: **~52 tokens/s** generation
- **60% performance boost!**

---

## Step-by-Step Setup

### 1. Launch LM Studio
```bash
open "/Applications/LM Studio.app"
```

### 2. **SET ENGINE TO MLX** ⭐ CRITICAL!

**Location:** Right panel → "Hardware Acceleration" dropdown

**Change from:**
- ❌ "Default" (uses llama.cpp)
- ❌ "CPU only"

**Change to:**
- ✅ **"MLX (Apple Silicon GPU)"**

This is THE most important setting. Everything else is secondary.

---

## 3. Point LM Studio to Your Models

**Method A: Add Path**
1. Click Settings (⚙️) in bottom left
2. Go to "Models" tab
3. Click "Add Path"
4. Navigate to: `/Users/jonathanmallinger/models/mlx`
5. Click "Select"

**Method B: Download Directly in LM Studio**
1. Click "Search" (🔍) at top
2. Type: `mlx-community/Josiefied-Qwen3-8B-abliterated-v1-4bit`
3. Click "Download"

Your models will appear in the left sidebar.

---

## 4. Context Length Configuration

**For 7-8B models (4-bit):**
- Context length: **8192 tokens** (recommended)
- Can push to 16384 if needed
- Leave ~8GB for system

**For 14B models (4-bit):**
- Context length: **4096 tokens** (recommended)
- Can push to 8192 if needed
- Leave ~6GB for system

**For 32B models (4-bit):**
- Context length: **2048 tokens** (start here)
- Increase cautiously to 4096
- Watch memory usage!

**Settings location:**
- Right panel → "Context Length" slider
- Or type exact number

---

## 5. Enable Flash Attention

**For contexts > 4K:**
- ✅ Enable "Flash Attention"
- Reduces KV cache by up to 75%
- Makes long contexts feasible

**For contexts < 4K:**
- Optional (minimal benefit)

**Settings location:**
- Right panel → Advanced → "Flash Attention" toggle

---

## 6. GPU Settings

**GPU Offload:**
- Set to **Maximum** (or 100%)
- MLX automatically uses unified memory optimally

**Metal Acceleration:**
- ✅ Auto-enabled with MLX engine
- No manual configuration needed

---

## 7. Sampling Parameters

**For Security Research / Uncensored:**
- **Temperature:** 0.7 - 0.9 (higher = more creative/uncensored)
- **Top-p:** 0.9 - 0.95
- **Repeat Penalty:** 1.1
- **Min-p:** 0.05 (optional)

**For Precise/Factual:**
- **Temperature:** 0.3 - 0.5
- **Top-p:** 0.9
- **Repeat Penalty:** 1.0

**For Creative/Open-ended:**
- **Temperature:** 1.0 - 1.2
- **Top-p:** 0.95
- **Repeat Penalty:** 1.1 - 1.2

**Settings location:**
- Right panel → "Sampling" section

---

## 8. Prompt Caching (Automatic)

**LM Studio 0.3.4+ has automatic prompt caching:**
- Reuses computations from previous messages
- Follow-up responses are MUCH faster
- Works with both text and vision models
- No configuration needed!

---

## 9. Memory Management

**Monitor memory usage:**
- Activity Monitor → Memory tab
- Watch "Memory Pressure" gauge

**If memory pressure is high:**
1. Reduce context length
2. Use smaller model
3. Close other applications
4. Use 4-bit instead of 6-bit/8-bit

**Safe memory allocation:**
- 7B-8B models: Use up to 12GB
- 14B models: Use up to 16GB
- 32B models: Use up to 20GB (tight!)
- Always leave 4-6GB for system

---

## 10. Parallel Requests (Advanced)

**New in 2026: Continuous Batching**
- Process multiple requests simultaneously
- Available in mlx-engine 1.0.0+
- Significant throughput improvements

**Use case:**
- Running API server
- Multiple concurrent chats
- Batch processing

---

## Performance Optimization Checklist

### Critical (Do These First):
- [x] ✅ **Set engine to MLX** (most important!)
- [x] Point LM Studio to `/Users/jonathanmallinger/models/mlx`
- [x] Set appropriate context length
- [x] Enable GPU offload to maximum

### Important:
- [ ] Enable Flash Attention (for long contexts)
- [ ] Configure sampling parameters
- [ ] Close memory-intensive apps

### Optional:
- [ ] Enable "Unload model when inactive"
- [ ] Adjust chunk size for prompt processing
- [ ] Fine-tune temperature for your use case

---

## Model Selection in LM Studio

**For quick testing:**
- Load: `Josiefied-Qwen3-1.7B-abliterated`
- Speed: 55+ tokens/s
- RAM: ~1GB

**For balanced performance:**
- Load: `Josiefied-Qwen3-8B-abliterated`
- Speed: 50-65 tokens/s
- RAM: ~5GB

**For high quality:**
- Load: `DeepSeek-R1-Distill-Qwen-32B-4bit`
- Speed: 20-30 tokens/s
- RAM: ~19GB (tight on 24GB!)

**For coding:**
- Load: `Qwen3-Coder-7B-4bit`
- Speed: 55-65 tokens/s
- RAM: ~5GB

**For vision:**
- Load: `Llama-3.2-11B-Vision-abliterated-4bit`
- Speed: 40-50 tokens/s
- RAM: ~8GB
- **Note:** Needs mlx-vlm support

---

## Testing Your Configuration

### Quick Speed Test:

1. Load a model in LM Studio
2. Type a simple prompt: "Hello, how are you?"
3. Watch the token counter in bottom right
4. Expected speeds:
   - 1-3B: 80-120 tokens/s
   - 7-8B: 50-65 tokens/s
   - 14B: 35-45 tokens/s
   - 32B: 20-30 tokens/s

### If speeds are lower:
1. **Check engine is set to MLX** (most common issue!)
2. Close other apps (Chrome, video, etc.)
3. Reduce context length
4. Use 4-bit model instead of 6/8-bit

---

## Advanced: Prompt Processing Optimization

**Default chunk size: 512 tokens**
**Recommended: 8192 tokens**

**Benefit:** Up to 1.5x faster prefill on long prompts

**How to change:**
- Currently requires editing config files
- Look for "prompt_chunk_size" setting
- Future versions may expose in UI

---

## Troubleshooting

### Issue: "Model won't load"
**Fix:**
1. Check model folder has config.json
2. Verify model format (should be SafeTensors or GGUF)
3. Try "Refresh" in LM Studio
4. Check available RAM (need 2x model size free)

### Issue: "Slow inference (< 10 t/s on 7B model)"
**Fix:**
1. **Verify MLX engine is selected** ← CHECK THIS FIRST!
2. Close other memory-intensive apps
3. Reduce context length to 2048
4. Switch to 4-bit quantization

### Issue: "Out of memory errors"
**Fix:**
1. Use smaller model (7B instead of 14B)
2. Reduce context length
3. Use 3-bit or 4-bit quantization
4. Close other apps
5. Restart LM Studio

### Issue: "Censored responses despite abliterated model"
**Fix:**
1. Increase temperature to 0.8-1.0
2. Verify you loaded abliterated version (check model name)
3. Rephrase prompt academically
4. Try different model (each has different guardrail level)

### Issue: "Model not in list"
**Fix:**
1. Settings → Models → Add Path → select mlx folder
2. Click "Refresh"
3. Make sure model folder has proper structure:
   ```
   mlx/MODEL_NAME/
     ├── config.json
     ├── model.safetensors (or weights.safetensors)
     ├── tokenizer.json
     └── other files...
   ```

---

## Performance Monitoring

### Activity Monitor:
```bash
# Open Activity Monitor
open -a "Activity Monitor"

# Watch:
# - Memory → Memory Pressure (keep green/yellow)
# - GPU History → GPU usage (should be high)
# - CPU → should be moderate
```

### Terminal Monitoring:
```bash
# GPU usage
sudo powermetrics --samplers gpu_power -i 1000 -n 10

# Memory usage
watch -n 1 'ps aux | grep -i "lm studio" | head -5'
```

---

## Best Practices Summary

1. **ALWAYS use MLX engine** for Apple Silicon
2. Start with 7-8B models for testing
3. Keep 6-8GB RAM free for system
4. Use 4-bit quantization for most models
5. Enable Flash Attention for long contexts
6. Monitor memory pressure
7. Close unused applications
8. Test with small prompts first
9. Gradually increase context if needed
10. Cache frequently-used models locally

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  LM STUDIO QUICK SETTINGS - M4 PRO      │
├─────────────────────────────────────────┤
│ Engine: MLX (Apple Silicon GPU) ⭐      │
│ GPU Offload: Maximum                    │
│ Context Length:                         │
│   • 7B models: 8192                     │
│   • 14B models: 4096                    │
│   • 32B models: 2048-4096               │
│ Flash Attention: ✅ (if context > 4K)   │
│ Temperature: 0.7-0.9 (uncensored)       │
│ Top-p: 0.9-0.95                         │
│ Repeat Penalty: 1.1                     │
└─────────────────────────────────────────┘
```

---

## Expected Performance Targets

| Model Size | Speed Target | What to Expect |
|------------|--------------|----------------|
| 1-3B | 80-120 t/s | ⚡ Ultra-fast, instant responses |
| 4-7B | 50-80 t/s | 🚀 Fast, very responsive |
| 8B | 45-65 t/s | ⚡ Fast, responsive |
| 14B | 30-45 t/s | ✓ Good, usable for chat |
| 21B MoE | 30-40 t/s | ✓ Good, slower but capable |
| 32B | 20-30 t/s | ~ Slower, but high quality |

**If you're not hitting these speeds, CHECK YOUR ENGINE SETTING!**

---

## Resources

- LM Studio Download: https://lmstudio.ai/
- MLX Documentation: https://ml-explore.github.io/mlx/
- Model Catalog: See `COMPLETE_MODEL_CATALOG.md`
- Your models: `/Users/jonathanmallinger/models/mlx`

---

*Last updated: February 2026 | LM Studio 0.3.4+ | MLX 0.30.6*
