# Speculative Decoding Test Suite - Complete Overview

## 🎯 Purpose

This test suite provides **complete end-to-end validation** of your speculative decoding setup, measuring performance, identifying optimal configurations, and ensuring everything works correctly.

## 📦 What's Included

### Main Test Script
- **`test_speculative_complete.py`** (24KB)
  - Complete automated test suite
  - Tests all configurations
  - Measures performance metrics
  - Generates comprehensive reports
  - Auto-detects running servers
  - Beautiful visual output (with `rich`)

### Documentation
- **`RUN_TESTS.md`** - Quick start guide
- **`TESTING_GUIDE.md`** - Detailed documentation
- **`QUICK_REFERENCE.md`** - One-page reference card

### Examples
- **`example_test_output.txt`** - What to expect when running
- **`example_test_results.json`** - Sample JSON report

## 🚀 Quick Start

### 1. Start the Server
```bash
python test_speculative.py
```

### 2. Run the Tests
```bash
python test_speculative_complete.py
```

### 3. Check Results
```bash
cat test_results.json
```

**That's it!** The script handles everything automatically.

## 📊 What Gets Tested

### 1. Server Availability (auto-detect)
- ✅ Speculative server (port 8000)
- ✅ LM Studio (port 1234)
- ✅ MLX Server (port 11434)

### 2. Configuration Performance
Tests all speculative configurations:
- **Baseline**: No speculative (reference point)
- **3 tokens**: Light speculative decoding
- **5 tokens**: Moderate (usually optimal)
- **7 tokens**: Aggressive speculative

**Measures**:
- Tokens per second
- Total generation time
- Speedup percentage
- Identifies best configuration

### 3. Prompt Type Optimization
Tests which tasks benefit most:
- **Security**: Research and vulnerability queries
- **Code**: Function implementations
- **Technical**: Detailed explanations
- **Creative**: Problem-solving

**Shows**:
- Baseline vs speculative performance
- Which tasks get biggest speedup
- Optimal use cases

### 4. System Prompt Impact
Compares different prompts:
- **Anti-refusal**: Direct, helpful responses
- **Empty**: No system prompt
- **Expert**: Detailed expert responses
- **Concise**: Brief answers

**Tests**:
- Performance impact
- Output quality
- Token efficiency

### 5. Comprehensive Reporting
Generates detailed JSON with:
- All performance metrics
- Configuration recommendations
- Best use case identification
- Speedup calculations
- Response previews

## 📈 Expected Results

### Typical Performance
```
Baseline (no spec):    18.2 tok/s
Speculative (3 tok):   24.1 tok/s (+32%)
Speculative (5 tok):   29.8 tok/s (+64%)  ⭐ BEST
Speculative (7 tok):   27.3 tok/s (+50%)
```

### Speedup Ranges
- **Excellent**: 50-70% speedup
- **Good**: 30-50% speedup
- **Moderate**: 15-30% speedup
- **Poor**: 0-15% speedup

### Best Use Cases
1. 🏆 Technical explanations (60-70%)
2. 💻 Code generation (50-65%)
3. 🔒 Security queries (45-55%)
4. 🎨 Creative tasks (30-45%)

## 🎨 Visual Output

### With `rich` (recommended)
```bash
pip install rich
```
You get:
- ✨ Beautiful tables with borders
- 🎨 Color-coded output (green/red/yellow)
- 📊 Progress indicators
- 📦 Formatted panels
- ⭐ Best configuration highlights

### Without `rich`
- ✅ Plain text tables
- 📝 Simple formatting
- ✓ Fully functional
- ☑ All features work

## 📁 Output Files

### `test_results.json`
Complete performance data:
```json
{
  "timestamp": "2026-02-10 14:30:45",
  "configuration_tests": [...],
  "prompt_type_tests": {...},
  "system_prompt_tests": {...},
  "recommendations": {
    "best_configuration": {...},
    "best_use_case": {...}
  }
}
```

## ⏱️ Test Duration

- **Server check**: 5 seconds
- **Configuration tests**: ~5 minutes
- **Prompt type tests**: ~8 minutes
- **System prompt tests**: ~3 minutes
- **Report generation**: 1 second

**Total**: ~15-20 minutes for complete suite

## 🔍 Key Features

### Auto-Detection
- ✅ Automatically finds running servers
- ✅ Tests each available endpoint
- ✅ Reports which are working
- ✅ Gracefully handles failures

### Performance Measurement
- ⚡ Tokens per second
- ⏱️ Time to first token (estimated)
- ⏰ Total generation time
- 📊 Speedup percentages
- 🎯 Best configuration identification

### Comprehensive Testing
- 📝 4 diverse prompt types
- ⚙️ 4 configuration options
- 💬 4 system prompt variations
- 🔄 Multiple test runs per configuration

### Smart Recommendations
- 🏆 Best overall configuration
- 💡 Optimal use cases
- 📈 Expected performance gains
- ⚠️ Warning signs to watch for

### Visual Feedback
- ✅ Success indicators
- ❌ Error messages
- ⚠️ Warnings
- 📊 Progress updates
- 🎯 Highlights

## 🛠️ Troubleshooting

### Server Not Running
```bash
❌ Speculative server is not running!
```
**Fix**: Start with `python test_speculative.py`

### Connection Timeout
```bash
❌ NOT RUNNING - Timeout
```
**Fix**: Check firewall, restart server, verify port

### Slow Performance
```bash
⚠️ Only 10 tok/s - expected 18+
```
**Fix**: Close apps, check GPU, reduce draft tokens

### Import Errors
```bash
ImportError: No module named 'requests'
```
**Fix**: `pip install requests rich`

## 📋 Recommendations

### After Testing

1. ✅ **Note the best configuration**
   - Usually 5 draft tokens
   - Check your specific results
   - May vary by hardware

2. ✅ **Update production config**
   ```bash
   --num-speculative-tokens 5
   ```

3. ✅ **Test with real workload**
   - Use your actual prompts
   - Measure production performance
   - Compare with test results

4. ✅ **Monitor over time**
   - Save test results
   - Re-run after changes
   - Track performance trends

5. ✅ **Optimize further**
   - Try different draft models
   - Adjust token counts
   - Fine-tune for your use case

## 🎯 Use Cases

### Perfect For
- ✅ Validating new setup
- ✅ Comparing configurations
- ✅ Identifying optimal settings
- ✅ Performance benchmarking
- ✅ Before production deployment

### Run Tests When
- 🔄 Setting up initially
- 🔄 Changing models
- 🔄 Updating configuration
- 🔄 Troubleshooting performance
- 🔄 Hardware changes

## 📊 Interpreting Results

### Configuration Tests
Shows raw performance across settings:
- Baseline establishes reference
- 3 tokens shows light overhead
- 5 tokens usually optimal balance
- 7 tokens tests aggressive speculation

### Prompt Type Tests
Reveals which tasks benefit most:
- Predictable tasks: high speedup
- Creative tasks: moderate speedup
- Helps optimize use cases

### System Prompt Tests
Balances quality vs performance:
- Expert prompts: longer, detailed
- Concise prompts: shorter, faster
- Choose based on needs

### Recommendations
Automated analysis suggests:
- Best configuration for speed
- Optimal use cases
- Expected performance gains

## 🚀 Production Deployment

### Use Optimal Settings
```bash
python -m vllm.entrypoints.openai.api_server \
    --model deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
    --speculative-model Qwen/Qwen2.5-1.5B-Instruct \
    --num-speculative-tokens 5 \
    --use-v2-block-manager \
    --disable-log-requests
```

### Monitor Performance
- Track tokens/sec in production
- Compare with test results
- Alert if performance degrades
- Re-run tests if issues arise

### Continuous Improvement
- Test new models
- Experiment with settings
- Measure real-world impact
- Iterate based on results

## 📚 Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `RUN_TESTS.md` | Quick start | Before first run |
| `TESTING_GUIDE.md` | Detailed guide | For deep understanding |
| `QUICK_REFERENCE.md` | One-page cheat sheet | During testing |
| `example_test_output.txt` | Sample output | To see what to expect |
| `example_test_results.json` | Sample results | To understand JSON format |

## 💡 Pro Tips

1. **Install `rich`** for better visuals
   ```bash
   pip install rich
   ```

2. **Save results over time**
   ```bash
   cp test_results.json results_$(date +%Y%m%d).json
   ```

3. **Test with your prompts**
   - Edit `test_prompts` in script
   - Add your actual use cases
   - Measure real-world benefit

4. **Run regularly**
   - After model updates
   - When changing hardware
   - To validate changes

5. **Compare configurations**
   - Save baseline results
   - Test different draft models
   - Find your optimal setup

## 🎓 Learning from Results

### High Speedup (50-70%)
✅ Excellent model pairing
✅ Hardware working well
✅ Optimal configuration
✅ Use these settings!

### Moderate Speedup (30-50%)
✅ Good performance
✅ Consider fine-tuning
✅ Safe for production
✅ Minor optimization possible

### Low Speedup (0-30%)
⚠️ Overhead too high
⚠️ Try different draft model
⚠️ Reduce draft tokens
⚠️ Check GPU utilization

### Negative Speedup
❌ Configuration issue
❌ Disable speculative
❌ Use baseline instead
❌ Review setup

## 📞 Getting Help

### Before Asking
1. ✅ Read `TESTING_GUIDE.md`
2. ✅ Check `QUICK_REFERENCE.md`
3. ✅ Review error messages
4. ✅ Examine server logs
5. ✅ Compare with examples

### Common Issues
- Server not starting → Check models downloaded
- Slow performance → Check GPU usage
- Connection errors → Verify ports not blocked
- Import errors → Install dependencies

## 🎉 Success Criteria

You'll know it's working when:
- ✅ All servers detected
- ✅ Tests complete without errors
- ✅ Speedup > 30%
- ✅ Report generated
- ✅ Recommendations clear

## 📈 Next Steps

1. **Run the tests** - Start with quick validation
2. **Review results** - Check recommendations
3. **Update config** - Use optimal settings
4. **Deploy** - Use in production
5. **Monitor** - Track real-world performance
6. **Iterate** - Re-test and optimize

## 🌟 Summary

This test suite provides:
- ✨ Complete validation of setup
- 📊 Performance benchmarking
- 🎯 Optimal configuration identification
- 💡 Use case recommendations
- 📈 Comprehensive reporting

All in **one simple command**:
```bash
python test_speculative_complete.py
```

Happy testing! 🚀

---

**Created**: 2026-02-10
**Version**: 1.0
**Status**: Production Ready ✅
