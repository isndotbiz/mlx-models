# Speculative Decoding Presets

Quick-start scripts for running MLX models with speculative decoding.

## Available Presets

### speculative-fast.sh
- Draft tokens: 3
- Best for: Interactive chat, quick responses
- Expected speedup: ~1.5x

### speculative-balanced.sh (RECOMMENDED)
- Draft tokens: 5
- Best for: General use, coding, most tasks
- Expected speedup: ~2x

### speculative-max.sh
- Draft tokens: 7
- Best for: Long generations, bulk processing
- Expected speedup: ~2.5-3x

## Usage

```bash
# From the models directory
./start-speculative.sh [fast|balanced|max]

# Or run directly
./presets/speculative-balanced.sh
```

## System Prompts

Located in `prompts/` subdirectory:

- **anti-refusal.txt**: Best uncensored prompt (recommended)
- **expert.txt**: Expert-level technical responses
- **empty.txt**: No system guidance

## Customization

Edit any preset script to change:
- Number of draft tokens (`--num-draft-tokens`)
- Port (`--port`)
- Host (`--host`)
- Model paths

All scripts include automatic port fallback (8000 → 8080) if ports are busy.
