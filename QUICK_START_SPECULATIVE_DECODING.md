# Quick Start: Enable Speculative Decoding in LM Studio

## What I've Done

✅ Modified LM Studio settings to enable speculative decoding options
✅ Verified both models are available and compatible
✅ Tested baseline performance (18 tok/s)

## What You Need to Do (2 Minutes)

### Option A: Via Chat Interface (Easiest)

1. **Open LM Studio** (if not already open)

2. **Go to Chat tab**

3. **Look for Model Settings** in the right sidebar or model configuration panel

4. **Find "Speculative Decoding" section** (should be visible now after settings change)

5. **Enable it and select:**
   - Draft Model: `josiefied-qwen2.5-0.5b-abliterated`

6. **Done!** Try generating text and watch for speed improvements

### Option B: Via Model Loader

1. **Click the Model Loader icon** (🔧 or similar)

2. **Select your main model** in the list

3. **Click "Load Settings" or "Advanced"**

4. **Find "Speculative Decoding"**

5. **Enable and select draft model:** `josiefied-qwen2.5-0.5b-abliterated`

6. **Apply/Save**

## Expected Results

- **Speed boost:** 20-50% faster (from ~18 to ~22-27 tok/s)
- **Visual indicator:** Draft model badge/indicator in UI
- **Visualization:** See which tokens came from draft vs main model (if enabled)

## Test It

After enabling, try this in the LM Studio chat:

**Prompt:** "Write a detailed explanation of how neural networks work."

You should see:
- Faster generation
- Draft model indicator
- Token visualization (if enabled)

## Troubleshooting

**Don't see the option?**
1. Restart LM Studio (to reload settings)
2. Check that Developer Mode is ON in Settings
3. Look under "Advanced Settings" or "Performance"

**Not faster?**
1. Make sure the draft model is actually selected
2. Try longer generations (better speedup)
3. Check the visualization to confirm it's active

## Files Modified

- `/Users/jonathanmallinger/.lmstudio/settings.json`
  - Set `speculativeDecoding: true`
  - Set `visualizeSpeculativeDecoding: true`

## More Details

See `speculative_decoding_setup.md` for comprehensive documentation.

---

**Current Status:**
- Main Model: josiefied-qwen3-8b-abliterated-v1 ✅ Loaded
- Draft Model: josiefied-qwen2.5-0.5b-abliterated ✅ Available
- Settings: ✅ Configured
- Next: Enable in GUI (2 minutes)
