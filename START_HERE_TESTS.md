# 🚀 Speculative Decoding Test Suite - START HERE

## One-Line Quick Start

```bash
# Terminal 1: Start server
python test_speculative.py

# Terminal 2: Run tests (wait for server to start first)
python test_speculative_complete.py
```

## What You Get

✅ **Complete validation** of your speculative decoding setup
✅ **Performance benchmarks** across all configurations
✅ **Optimal settings** identified automatically
✅ **Detailed report** saved to JSON
✅ **Visual feedback** throughout testing

## Installation (One Time)

```bash
# Required
pip install requests

# Optional (for beautiful output)
pip install rich
```

## Expected Output

```
Testing Speculative Decoding Setup
===================================

Server Status:
✅ Speculative (port 8000): RUNNING

Performance Tests:
------------------
Baseline (no spec):    18.2 tok/s
Speculative (3 tok):   24.1 tok/s (+32%)
Speculative (5 tok):   29.8 tok/s (+64%)  ⭐ BEST
Speculative (7 tok):   27.3 tok/s (+50%)

🏆 Recommended Configuration: 5 draft tokens
   Performance: 29.8 tokens/sec
   Speedup: +64% vs baseline
```

## What Gets Tested

1. ✅ **Server availability** - Auto-detects all running servers
2. ⚡ **Configuration performance** - Tests 0/3/5/7 draft tokens
3. 📝 **Prompt types** - Security, code, technical, creative
4. 💬 **System prompts** - Anti-refusal, expert, concise, empty
5. 📊 **Report generation** - Complete JSON with recommendations

## Time Required

⏱️ **15-20 minutes** for complete test suite

## Output Files

| File | Contains |
|------|----------|
| `test_results.json` | Complete performance data & recommendations |

## Next Steps After Testing

1. ✅ Check `test_results.json` for detailed metrics
2. ✅ Note the recommended configuration (usually 5 tokens)
3. ✅ Update your server startup with optimal settings
4. ✅ Test with your real workload

## Production Deployment

Use the recommended settings:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --speculative-model Qwen/Qwen2.5-1.5B-Instruct \
    --num-speculative-tokens 5 \
    --use-v2-block-manager \
    --disable-log-requests
```

## Documentation

| File | When to Read |
|------|--------------|
| **START_HERE_TESTS.md** (this file) | Right now! |
| `RUN_TESTS.md` | Before running tests |
| `QUICK_REFERENCE.md` | During testing |
| `TESTING_GUIDE.md` | For detailed info |
| `TEST_SUITE_OVERVIEW.md` | Complete reference |

## Troubleshooting

### Server Not Running?
```bash
python test_speculative.py
```

### Import Errors?
```bash
pip install requests rich
```

### Need Help?
Check `TESTING_GUIDE.md` for detailed troubleshooting.

## Success Criteria

You'll know it works when:
- ✅ Tests complete without errors
- ✅ Speedup > 30%
- ✅ Report generated
- ✅ Recommendations displayed

## Ready to Go!

```bash
# That's it - just run these two commands:
python test_speculative.py          # Terminal 1
python test_speculative_complete.py # Terminal 2
```

🎉 **Happy testing!**

---

**Quick Links**:
- 📖 Full Guide: `TESTING_GUIDE.md`
- 🎯 Quick Ref: `QUICK_REFERENCE.md`
- 📊 Overview: `TEST_SUITE_OVERVIEW.md`
- 🏃 Run Guide: `RUN_TESTS.md`
