# Speculative Decoding Testing Guide

## Quick Start

```bash
# Run the complete test suite
python test_speculative_complete.py
```

## What Gets Tested

### 1. Server Status Check
- ✅ Speculative server (port 8000)
- ✅ LM Studio (port 1234)
- ✅ MLX Server (port 11434)

### 2. Configuration Testing
Tests all speculative decoding configurations:
- **Baseline**: No speculative decoding (reference)
- **3 tokens**: Light speculative decoding
- **5 tokens**: Moderate speculative decoding (usually optimal)
- **7 tokens**: Aggressive speculative decoding

**Metrics measured**:
- Tokens per second
- Total generation time
- Speedup percentage vs baseline
- Identifies best configuration automatically

### 3. Prompt Type Testing
Tests how different tasks benefit from speculative decoding:
- **Security research**: Technical query about vulnerabilities
- **Code generation**: Function implementation with types
- **Technical explanation**: Detailed ML/AI concepts
- **Creative problem-solving**: Open-ended reasoning

**Shows which tasks get biggest speedup!**

### 4. System Prompt Testing
Compares different system prompts:
- **Anti-refusal**: Direct, no-refusal prompt
- **Empty**: No system prompt
- **Expert**: Expert assistant prompt
- **Concise**: Brief response prompt

Tests both performance and output quality.

### 5. Report Generation
Creates `test_results.json` with:
- All performance metrics
- Speedup calculations
- Best configuration recommendation
- Best use case identification
- Detailed timing breakdowns

## Understanding the Output

### Server Status
```
Server Status Check
===================
✅ Speculative Server (port 8000): RUNNING
✅ LM Studio (port 1234): RUNNING
❌ MLX Server (port 11434): NOT RUNNING - Connection refused
```

### Performance Comparison
```
┌───────────────────────────────────────────────────┐
│       Speculative Decoding Performance            │
├──────────────┬──────────┬────────┬─────────┬──────┤
│ Config       │ Tok/Sec  │ Time   │ Speedup │ Best │
├──────────────┼──────────┼────────┼─────────┼──────┤
│ No spec      │    18.2  │ 13.74s │ baseline│      │
│ 3 tokens     │    24.1  │ 10.37s │  +32%   │      │
│ 5 tokens     │    29.8  │  8.39s │  +64%   │ ⭐   │
│ 7 tokens     │    27.3  │  9.16s │  +50%   │      │
└──────────────┴──────────┴────────┴─────────┴──────┘
```

### Prompt Type Comparison
```
┌─────────────────────────────────────────────────┐
│        Performance by Prompt Type               │
├──────────────┬──────────┬────────────┬─────────┤
│ Type         │ Baseline │ Speculative│ Speedup │
├──────────────┼──────────┼────────────┼─────────┤
│ Security     │   18.5   │    28.2    │  +53%   │
│ Code gen     │   19.1   │    31.4    │  +64%   │
│ Technical    │   17.8   │    29.8    │  +67%   │
│ Creative     │   18.9   │    27.1    │  +43%   │
└──────────────┴──────────┴────────────┴─────────┘
```

## Recommendations Section

The test automatically identifies:

1. **Best Configuration**: Optimal number of draft tokens
2. **Best Use Case**: Which prompt type benefits most
3. **Performance Gains**: Expected speedup for your workload

Example:
```
🏆 Recommended Configuration: 5 draft tokens
   Performance: 29.8 tokens/sec
   Speedup: +64% vs baseline

💡 Best Use Case: Technical explanation
   Achieves +67% speedup with speculative decoding
```

## Installation

### Required
```bash
pip install requests
```

### Optional (for better visuals)
```bash
pip install rich
```

The script works without `rich`, but you get:
- ✨ Beautiful tables
- 🎨 Color-coded output
- 📊 Progress indicators
- 📦 Formatted panels

## What to Look For

### Good Results
- ✅ Speedup of 30-70% with speculative decoding
- ✅ 5 tokens usually optimal
- ✅ Bigger models benefit more
- ✅ Repetitive tasks see biggest gains

### Warning Signs
- ⚠️ Negative speedup (speculative slower than baseline)
- ⚠️ Server connection errors
- ⚠️ Very low tokens/sec (< 10 tok/s)

### Troubleshooting

**Server not responding?**
```bash
# Check if running
lsof -i :8000

# Restart server
python test_speculative.py
```

**Slow performance?**
- Check CPU/GPU usage
- Close other applications
- Try smaller draft model
- Reduce number of draft tokens

**Connection errors?**
- Verify server is running
- Check firewall settings
- Ensure correct port numbers

## Advanced Usage

### Test specific server only
Edit the script to change default server:
```python
config_results = suite.test_speculative_configurations('lm_studio')
```

### Test with different prompts
Add custom prompts to `test_prompts` dictionary:
```python
self.test_prompts['custom'] = {
    'prompt': "Your custom prompt here",
    'description': "Custom test",
    'expected_tokens': 200
}
```

### Change output file
```python
suite.generate_report(results, output_file="my_results.json")
```

## Interpreting Results

### Speedup Patterns

**High speedup (50-70%)**:
- Predictable text generation
- Code completion
- Templated responses
- Technical documentation

**Moderate speedup (30-50%)**:
- General Q&A
- Mixed content types
- Varied vocabulary

**Low speedup (0-30%)**:
- Highly creative tasks
- Unpredictable outputs
- Very short responses

### Optimal Configuration

Most common results:
- **3 tokens**: 20-35% speedup, low overhead
- **5 tokens**: 40-65% speedup, best balance ⭐
- **7 tokens**: 30-55% speedup, higher overhead

**Rule of thumb**: Start with 5, adjust based on results.

## Next Steps

After running tests:

1. **Check `test_results.json`** for detailed metrics
2. **Note the recommended configuration**
3. **Update your server startup** with optimal settings
4. **Test with your actual workload**
5. **Monitor performance in production**

## Production Deployment

Use the optimal settings found:

```bash
# Start with recommended config (usually 5 tokens)
python -m vllm.entrypoints.openai.api_server \
    --model deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --speculative-model Qwen/Qwen2.5-1.5B-Instruct \
    --num-speculative-tokens 5 \
    --use-v2-block-manager \
    --disable-log-requests
```

## Continuous Testing

Re-run tests when:
- ✅ Updating models
- ✅ Changing hardware
- ✅ Modifying configuration
- ✅ Testing new prompts
- ✅ Validating performance

Keep `test_results.json` for historical comparison!

## Support

If you encounter issues:
1. Check server logs
2. Verify model downloads
3. Test baseline (no speculative) first
4. Compare with test results
5. Check system resources

Happy testing! 🚀
