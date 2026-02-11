# Speculative Decoding Quick Reference

## 🚀 Quick Start

```bash
# Run complete test suite
python test_speculative_complete.py

# Check results
cat test_results.json
```

## 📊 What Gets Measured

| Test Type | What It Shows |
|-----------|---------------|
| **Configuration** | Baseline vs 3/5/7 draft tokens |
| **Prompt Types** | Which tasks benefit most |
| **System Prompts** | Quality vs performance tradeoff |
| **Speedup** | Percentage improvement |

## 🎯 Expected Results

### Typical Speedup
- **No speculative**: Baseline (18-22 tok/s)
- **3 tokens**: +25-35% speedup
- **5 tokens**: +40-65% speedup ⭐ **OPTIMAL**
- **7 tokens**: +30-55% speedup

### Best Use Cases (highest speedup)
1. 🏆 Technical explanations
2. 💻 Code generation
3. 🔒 Security queries
4. 🎨 Creative tasks (lower benefit)

## 📁 Output Files

| File | Contains |
|------|----------|
| `test_results.json` | Full metrics and recommendations |
| `test_speculative_complete.py` | Test script |
| `TESTING_GUIDE.md` | Detailed documentation |

## 🔧 Common Commands

```bash
# Install dependencies
pip install requests rich

# Make executable
chmod +x test_speculative_complete.py

# Run tests
./test_speculative_complete.py

# Check if server is running
lsof -i :8000
```

## ⚡ Performance Checklist

- [ ] Server responds on port 8000
- [ ] Baseline performance > 15 tok/s
- [ ] Speculative speedup > 30%
- [ ] No connection errors
- [ ] Results saved to JSON

## 🎨 Visual Output

### With `rich` (recommended)
- ✨ Beautiful tables
- 🎨 Color-coded results
- 📊 Progress bars
- 📦 Formatted panels

### Without `rich`
- ✅ Plain text tables
- 📝 Simple formatting
- ✓ Still fully functional

## 📈 Interpreting Results

### Excellent (50-70% speedup)
✅ Configuration is optimal
✅ Models are well-matched
✅ Use in production

### Good (30-50% speedup)
✅ Working correctly
✅ Try adjusting draft tokens
✅ Safe for production

### Poor (0-30% speedup)
⚠️ Check model compatibility
⚠️ Verify GPU utilization
⚠️ Consider different draft model

### Negative speedup
❌ Overhead too high
❌ Disable speculative decoding
❌ Use baseline instead

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not found | Start with `python test_speculative.py` |
| Connection timeout | Check firewall/ports |
| Low performance | Close other apps, check GPU |
| Import errors | `pip install requests rich` |
| Permission denied | `chmod +x test_speculative_complete.py` |

## 📋 Test Sections

### 1. Server Status ✓
Checks if servers are running and responsive

### 2. Configuration Tests ⚙️
Tests baseline vs 3/5/7 draft tokens

### 3. Prompt Type Tests 📝
Measures speedup for different tasks

### 4. System Prompt Tests 💬
Compares different prompt strategies

### 5. Report Generation 📊
Creates JSON with all metrics

### 6. Recommendations 🎯
Suggests optimal configuration

## 🎯 Action Items

After running tests:

1. ✅ Note recommended configuration
2. ✅ Update server startup script
3. ✅ Test with real workload
4. ✅ Monitor production performance
5. ✅ Save results for comparison

## 📊 Sample Output

```
🏆 Recommended Configuration: 5 draft tokens
   Performance: 29.8 tokens/sec
   Speedup: +64% vs baseline

💡 Best Use Case: Technical explanation
   Achieves +67% speedup
```

## 🚀 Production Setup

Use optimal settings found:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --speculative-model Qwen/Qwen2.5-1.5B-Instruct \
    --num-speculative-tokens 5 \
    --use-v2-block-manager
```

## 📞 Need Help?

1. Check `TESTING_GUIDE.md` for details
2. Review `example_test_output.txt` for expected output
3. Examine `example_test_results.json` for sample data
4. Verify server logs for errors

## 💡 Pro Tips

- ✨ Run tests after model updates
- 📊 Compare results over time
- 🎯 Test with your actual prompts
- ⚡ 5 tokens usually optimal
- 🔄 Re-test after config changes

---

**Remember**: Speculative decoding trades slight accuracy for speed. Perfect for production where speed matters!
