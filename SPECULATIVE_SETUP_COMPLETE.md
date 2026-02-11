# Speculative Decoding Setup - COMPLETE

All infrastructure has been created and configured successfully!

## What Was Created

### 1. Startup Scripts
Location: `/Users/jonathanmallinger/models/`

- **start-speculative.sh** - Main launcher with preset selection
  - Usage: `./start-speculative.sh [fast|balanced|max]`
  - Default: balanced (5 draft tokens)
  - Auto port fallback: 8000 → 8080

- **test-speculative.sh** - Comprehensive test script
  - Tests server availability
  - Runs generation test
  - Measures tokens/sec performance

### 2. Preset Configurations
Location: `/Users/jonathanmallinger/models/presets/`

| Preset | Draft Tokens | Use Case | Expected Speedup |
|--------|--------------|----------|------------------|
| speculative-fast.sh | 3 | Interactive chat, quick queries | ~1.5x |
| speculative-balanced.sh | 5 | General use (RECOMMENDED) | ~2.0x |
| speculative-max.sh | 7 | Long generations, bulk processing | ~2.5-3x |

All presets:
- Auto-activate virtual environment
- Use same model family (Qwen2.5)
- Include port fallback logic
- Display clear startup information

### 3. System Prompt Presets
Location: `/Users/jonathanmallinger/models/presets/prompts/`

- **anti-refusal.txt** - Best uncensored prompt we found
  - Direct, honest answers without moral judgment
  - No unsolicited warnings or disclaimers
  - Maximally helpful approach

- **expert.txt** - Expert technical framing
  - Deep knowledge across domains
  - Technical accuracy and specificity
  - Comprehensive, detailed responses

- **empty.txt** - No system guidance
  - For testing or custom prompts

### 4. OpenCode Integration
Location: `/Users/jonathanmallinger/.config/opencode/opencode.json`

Updated with three speculative decoding variants:
```json
{
  "model": "speculative/qwen2.5-3b-speculative-balanced",
  "provider": {
    "speculative": {
      "models": {
        "qwen2.5-3b-speculative-balanced": "5 draft tokens (RECOMMENDED)",
        "qwen2.5-3b-speculative-fast": "3 draft tokens",
        "qwen2.5-3b-speculative-max": "7 draft tokens"
      }
    }
  }
}
```

Default model: `speculative/qwen2.5-3b-speculative-balanced`

### 5. Documentation
- **QUICK_START_SPECULATIVE.md** - Complete quick-start guide
  - One-command startup
  - How to test
  - Expected performance
  - Troubleshooting
  - Tips and best practices

- **presets/README.md** - Preset documentation

## Model Configuration

### Main Model
- **Name**: Josiefied-Qwen2.5-3B-abliterated
- **Path**: `/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-3B-abliterated`
- **Features**: High-quality, uncensored, good speed/quality balance
- **Why Qwen2.5**: Avoids Qwen3 bugs

### Draft Model
- **Name**: Josiefied-Qwen2.5-0.5B-abliterated
- **Path**: `/Users/jonathanmallinger/models/mlx/Josiefied-Qwen2.5-0.5B-abliterated`
- **Features**: Same family as main model, very fast
- **Why same family**: Optimal draft token acceptance rate

## Quick Start

```bash
# Start server (balanced preset - recommended)
cd /Users/jonathanmallinger/models
./start-speculative.sh

# In another terminal: Test it
./test-speculative.sh

# Use with OpenCode (already configured!)
# Just start OpenCode and it will connect to the speculative server
```

## Expected Performance

| Metric | Without Speculative | With Speculative (Balanced) |
|--------|---------------------|----------------------------|
| Tokens/sec | 25-35 | 50-60 |
| Speedup | 1.0x | ~2.0x |
| Quality | 100% | 100% (identical) |

## File Permissions

All scripts are executable:
```bash
-rwxr-xr-x  start-speculative.sh
-rwxr-xr-x  test-speculative.sh
-rwxr-xr-x  presets/speculative-fast.sh
-rwxr-xr-x  presets/speculative-balanced.sh
-rwxr-xr-x  presets/speculative-max.sh
```

## Features

### Automatic Port Fallback
- Primary: 8000
- Fallback: 8080
- Error if both busy

### Virtual Environment
- All scripts auto-activate: `/Users/jonathanmallinger/models/.venv`
- No manual activation needed

### Informative Output
- Clear startup messages
- Configuration display
- Server URL shown
- Test commands provided

## Integration Points

1. **OpenCode** - Already configured, just start the server
2. **Direct API** - Standard OpenAI-compatible endpoint at `http://localhost:8000/v1`
3. **Custom integrations** - Use any OpenAI-compatible client

## Validation

All components verified:
- [x] Preset scripts created and executable
- [x] System prompt files created
- [x] Main launcher created and executable
- [x] Test script created and executable
- [x] OpenCode config updated
- [x] Default model set to balanced preset
- [x] Documentation complete

## Next Steps

1. **Start the server**:
   ```bash
   ./start-speculative.sh
   ```

2. **Test it** (in another terminal):
   ```bash
   ./test-speculative.sh
   ```

3. **Expected output**:
   - Server responds to health checks
   - Generates text successfully
   - Shows ~50-60 tokens/sec (vs ~25-35 without speculative)
   - Draft token acceptance rate >60%

4. **Use it**:
   - With OpenCode (automatic)
   - With curl/scripts (http://localhost:8000/v1)
   - With any OpenAI-compatible client

## Troubleshooting Resources

See `QUICK_START_SPECULATIVE.md` for:
- Port conflicts
- Low performance
- Server start issues
- Draft token problems

## Tips for Best Results

1. Use the **balanced preset** for most tasks
2. Use **anti-refusal.txt** system prompt for best responses
3. Lower temperature = faster inference (more predictable)
4. Monitor draft token acceptance rate (aim for >60%)
5. Try different presets to find optimal for your use case

## Technical Details

### Speculative Decoding Process
1. Draft model generates N tokens quickly
2. Main model verifies tokens in parallel
3. Accepted tokens are used, rejected tokens regenerated
4. Net result: Much faster inference with identical quality

### Why Same Model Family?
- Higher acceptance rate (>60-80%)
- Better prediction alignment
- More consistent speedup

### Why These Token Counts?
- Fast (3): Low overhead, responsive
- Balanced (5): Optimal acceptance vs speedup
- Max (7): Maximum speed, may show diminishing returns

---

**Status**: Setup complete and ready to use!

**Run**: `./start-speculative.sh` to get started.
