# Speculative Decoding Setup for LM Studio

## Current Status

### Models Available
- **Main Model**: josiefied-qwen3-8b-abliterated-v1 (4.62 GB, currently loaded)
- **Draft Model**: josiefied-qwen2.5-0.5b-abliterated (293.99 MB, fastest at 235 tok/s)

### Configuration Changes Made
Modified `/Users/jonathanmallinger/.lmstudio/settings.json`:
1. Enabled speculative decoding in config presets: `"speculativeDecoding": true`
2. Enabled visualization: `"visualizeSpeculativeDecoding": true`

### LM Studio Environment
- Version: MLX-based inference (Apple Silicon optimized)
- Backend: mlx-llm-mac-arm64-apple-metal-advsimd-1.0.0
- Server: Running on port 1234
- Context Length: 40960 tokens
- Compatible draft models detected in cache

## How to Enable Speculative Decoding (GUI Method)

Since the CLI doesn't support speculative decoding configuration yet, you need to use the LM Studio GUI:

### Step 1: Enable Developer/Power User Mode (If Not Already Enabled)
1. Open LM Studio
2. Go to **Settings** (⚙️ icon in the sidebar)
3. Find **Developer Mode** or **User Interface Complexity Level**
4. Set to **Power User** or **Developer Mode**

### Step 2: Configure Speculative Decoding in Chat
1. Click on the **Chat** tab in LM Studio
2. In the chat sidebar, look for the model configuration section
3. You should now see a **Speculative Decoding** section (enabled by the config changes)
4. Click to expand it
5. Enable speculative decoding by toggling it ON
6. Select the draft model: **josiefied-qwen2.5-0.5b-abliterated**

### Step 3: Alternative - Configure in Model Loader
1. Go to the **Model Loader** (🔧 icon)
2. Select your main model: **josiefied-qwen3-8b-abliterated-v1**
3. Look for **Advanced Settings** or **Performance Settings**
4. Find **Speculative Decoding** section
5. Enable it and select the draft model

### Step 4: Verify Configuration
After enabling, you should see:
- A draft model indicator in the chat interface
- The `fromDraftModel` field in responses showing which tokens came from draft vs main model
- Visualization (if enabled) showing draft/main model token attribution

## Expected Performance Gains

### Without Speculative Decoding
- Current speed: ~18 tokens/second (from conversation logs)
- Single model inference

### With Speculative Decoding
- Expected speed: **22-27 tokens/second** (20-50% improvement)
- Draft model generates speculative tokens at 235 tok/s
- Main model validates/corrects in parallel
- Best gains on longer, predictable text generation

## Compatibility Information

According to the draft model compatibility cache, these models are compatible:
- ✅ mlx-community/Josiefied-Qwen2.5-0.5B-abliterated (RECOMMENDED - fastest)
- ✅ mlx-community/Josiefied-Qwen2.5-3B-abliterated
- ✅ mlx-community/Qwen3-4B-4bit
- ✅ mlx-community/Josiefied-Qwen3-1.7B-abliterated-v1-4bit

## Testing the Setup

### Test 1: Baseline Performance (Already Tested)
```bash
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "josiefied-qwen3-8b-abliterated-v1",
    "messages": [{"role": "user", "content": "Explain SQL injection in one sentence."}],
    "max_tokens": 50,
    "stream": false
  }' | python3 -m json.tool
```

Result: Generated 49 tokens (completion only)

### Test 2: After Enabling Speculative Decoding
Run the same test and compare:
- Token generation speed (should be 20-50% faster)
- Check for `fromDraftModel` indicators in response
- Monitor the visualization in the GUI

### Test 3: Longer Generation (Better Speedup)
```bash
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "josiefied-qwen3-8b-abliterated-v1",
    "messages": [{"role": "user", "content": "Write a detailed explanation of how neural networks work, including backpropagation."}],
    "max_tokens": 200,
    "stream": true
  }'
```

Longer generations typically show better speedup with speculative decoding.

## Troubleshooting

### If Speculative Decoding Option Doesn't Appear
1. Restart LM Studio to reload settings.json changes
2. Check that both models are downloaded (they are)
3. Ensure you're using MLX-compatible models (you are)
4. Try switching to the Chat tab and back

### If Performance Doesn't Improve
1. Check that the draft model is actually loaded (look for memory usage increase)
2. Verify visualization is showing draft model tokens
3. Try with longer text generation (better gains)
4. Check system resources (ensure enough RAM/VRAM)

### If Models Aren't Compatible
The compatibility cache shows your models ARE compatible, but if you see errors:
1. Try a different draft model from the compatible list
2. Ensure both models use the same tokenizer (Qwen models should match)
3. Check LM Studio logs in the server output

## Configuration Files Modified

1. **Main Settings**: `/Users/jonathanmallinger/.lmstudio/settings.json`
   - Enabled speculative decoding visibility
   - Enabled visualization

2. **Draft Model Cache**: `/Users/jonathanmallinger/.lmstudio/.internal/draft-model-compatibility-cache.json`
   - Already contains compatibility information
   - Lists compatible draft models

## Next Steps

1. **Open LM Studio GUI** and follow the steps above to enable speculative decoding
2. **Select the draft model** (josiefied-qwen2.5-0.5b-abliterated)
3. **Run benchmark tests** before and after to measure speedup
4. **Monitor the visualization** to see how many tokens are accepted from the draft model

## Notes

- Speculative decoding works best with similar model architectures (same family)
- The 0.5B draft model is optimal for speed while maintaining accuracy
- MLX backend is optimized for Apple Silicon, providing additional performance benefits
- The acceptance rate of draft tokens depends on how "predictable" the text is

## Files and Paths Reference

- LM Studio Settings: `/Users/jonathanmallinger/.lmstudio/settings.json`
- Model Directory: `/Users/jonathanmallinger/.lmstudio/models/mlx-community/`
- Main Model: `Josiefied-Qwen3-8B-abliterated-v1-4bit`
- Draft Model: `Josiefied-Qwen2.5-0.5B-abliterated`
- Server: `http://localhost:1234`
- CLI: `~/.lmstudio/bin/lms`

