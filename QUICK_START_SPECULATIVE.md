# Speculative Decoding Quick Start Guide

Complete setup for speculative decoding with MLX - get 1.5-3x faster inference!

## What is Speculative Decoding?

Speculative decoding uses a small, fast "draft" model to predict multiple tokens at once, which are then verified by the main model. This dramatically speeds up inference (40-60+ tokens/sec vs 25-35 tokens/sec) with no quality loss.

## One-Command Startup

```bash
# Recommended: Balanced preset (5 draft tokens)
./start-speculative.sh

# Or choose a specific preset:
./start-speculative.sh fast      # 3 draft tokens - quick responses
./start-speculative.sh balanced  # 5 draft tokens - RECOMMENDED
./start-speculative.sh max       # 7 draft tokens - maximum speed
```

That's it! The server will start on port 8000 (or 8080 if 8000 is busy).

## Model Configuration

- **Main Model**: Josiefied-Qwen2.5-3B-abliterated
  - High-quality, uncensored responses
  - Good balance of speed and quality
  - Uses Qwen2.5 (no Qwen3 bugs)

- **Draft Model**: Josiefied-Qwen2.5-0.5B-abliterated
  - Same family as main model (optimal compatibility)
  - Very fast for draft generation
  - Abliterated for consistency

## Presets Explained

### Fast (3 draft tokens)
```bash
./presets/speculative-fast.sh
```
- Best for: Interactive chat, quick queries
- Speed: ~1.5x faster
- Lower overhead, more responsive

### Balanced (5 draft tokens) - RECOMMENDED
```bash
./presets/speculative-balanced.sh
```
- Best for: General use, coding assistance, most tasks
- Speed: ~2x faster
- Optimal balance of speed and efficiency

### Max (7 draft tokens)
```bash
./presets/speculative-max.sh
```
- Best for: Long generations, bulk processing
- Speed: ~2.5-3x faster
- Maximum speedup, may show diminishing returns

## Testing the Setup

### Quick Test
```bash
./test-speculative.sh
```

This will:
1. Check server availability
2. Get model information
3. Run a generation test
4. Measure tokens/sec

### Manual Test
```bash
# Check server status
curl http://localhost:8000/v1/models

# Test generation
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate fibonacci numbers",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

## Expected Performance

| Configuration | Tokens/sec | Speedup |
|--------------|------------|---------|
| No speculative decoding | 25-35 | 1.0x |
| Fast (3 draft tokens) | 40-50 | 1.5x |
| Balanced (5 draft tokens) | 50-60 | 2.0x |
| Max (7 draft tokens) | 60-70+ | 2.5x |

Actual performance depends on:
- Your hardware (M-series chip)
- Available RAM
- Current system load
- Prompt complexity

## System Prompt Presets

Located in `/Users/jonathanmallinger/models/presets/prompts/`:

### anti-refusal.txt
The best system prompt we found for uncensored, direct responses without moral lecturing.

```bash
# Use with API:
SYSTEM_PROMPT=$(cat /Users/jonathanmallinger/models/presets/prompts/anti-refusal.txt)
```

### expert.txt
Expert framing for technical, detailed responses with deep knowledge.

### empty.txt
Empty prompt for no system-level guidance.

## OpenCode Integration

The OpenCode config has been updated with three speculative decoding variants:

```json
{
  "model": "speculative/qwen2.5-3b-speculative-balanced"
}
```

Available models in OpenCode:
- `speculative/qwen2.5-3b-speculative-balanced` (default, recommended)
- `speculative/qwen2.5-3b-speculative-fast`
- `speculative/qwen2.5-3b-speculative-max`

Just start the server with your chosen preset, and OpenCode will automatically use it.

## Troubleshooting

### Port Already in Use
The scripts automatically try port 8080 if 8000 is busy. If both are busy:
```bash
# Find what's using the ports
lsof -i :8000
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Low Performance
1. Check if draft model is actually being used (should see it in server logs)
2. Try different preset (balanced usually best)
3. Close other resource-intensive apps
4. Check Activity Monitor for high CPU/memory usage

### Server Won't Start
```bash
# Activate virtual environment manually
source /Users/jonathanmallinger/models/.venv/bin/activate

# Check if models exist
ls -la /Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-*

# Try starting directly
mlx_lm.server --help
```

### Draft Tokens Not Accepted
If the server logs show very low acceptance rate:
- This is normal with unrelated models
- Our models are from the same family (optimal)
- Try the fast preset (fewer tokens = higher acceptance)

## Advanced Usage

### Custom Configuration
Edit the preset scripts in `/Users/jonathanmallinger/models/presets/` to customize:
- Number of draft tokens
- Port
- Host (for network access)
- Model paths

### Monitoring Performance
```bash
# Server logs show draft token acceptance rate
# Look for lines like:
# "Draft tokens accepted: 4/5 (80%)"
```

High acceptance rate (>60%) means speculative decoding is working well!

### Multiple Models
To run different models simultaneously:
1. Start first server on port 8000
2. Edit another preset script to use port 8001
3. Start second server

## Files Created

```
/Users/jonathanmallinger/models/
├── start-speculative.sh           # Main launcher
├── test-speculative.sh            # Test script
├── presets/
│   ├── speculative-fast.sh        # 3 draft tokens
│   ├── speculative-balanced.sh    # 5 draft tokens (recommended)
│   ├── speculative-max.sh         # 7 draft tokens
│   └── prompts/
│       ├── anti-refusal.txt       # Best uncensored prompt
│       ├── expert.txt             # Expert framing
│       └── empty.txt              # No system prompt
└── QUICK_START_SPECULATIVE.md     # This file
```

## Next Steps

1. **Start the server**: `./start-speculative.sh`
2. **Test it**: `./test-speculative.sh`
3. **Use with OpenCode**: It's already configured!
4. **Experiment**: Try different presets to find what works best for you

## Tips for Best Performance

1. **Use balanced preset** unless you have specific needs
2. **System prompts matter** - the anti-refusal prompt gives best results
3. **Temperature affects speed** - lower temperature = faster (more predictable)
4. **Longer prompts help** - draft model works better with more context
5. **Monitor acceptance rate** - high rate = good speedup

## Resources

- MLX Documentation: https://ml-explore.github.io/mlx/
- Speculative Decoding Paper: https://arxiv.org/abs/2211.17192
- Model Cards:
  - Main: https://huggingface.co/mlx-community/Josiefied-Qwen2.5-3B-abliterated
  - Draft: https://huggingface.co/mlx-community/Josiefied-Qwen2.5-0.5B-abliterated

---

**Questions?** Check the troubleshooting section or examine the preset scripts to see exactly what's running.
