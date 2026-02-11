# How to Run the Complete Test Suite

## Prerequisites

1. **Start the Speculative Server**
   ```bash
   python test_speculative.py
   ```
   Wait for "Server started successfully" message.

2. **Install Optional Dependencies** (recommended for better visuals)
   ```bash
   pip install rich
   ```

## Run the Tests

### Option 1: Direct Execution
```bash
python test_speculative_complete.py
```

### Option 2: Make it executable first
```bash
chmod +x test_speculative_complete.py
./test_speculative_complete.py
```

## What Happens

The script will automatically:

1. ✅ **Check Server Status**
   - Verifies all servers are running
   - Tests connections
   - Reports which are available

2. ⚡ **Test Configurations** (~5 minutes)
   - Baseline (no speculative)
   - 3 draft tokens
   - 5 draft tokens
   - 7 draft tokens

3. 📝 **Test Prompt Types** (~8 minutes)
   - Security queries
   - Code generation
   - Technical explanations
   - Creative tasks

4. 💬 **Test System Prompts** (~3 minutes)
   - Anti-refusal prompt
   - Empty prompt
   - Expert prompt
   - Concise prompt

5. 📊 **Generate Report**
   - Creates `test_results.json`
   - Shows recommendations
   - Displays best configuration

**Total Time**: ~15-20 minutes

## Expected Output

You'll see:
- ✅ Green checkmarks for successful tests
- 📊 Performance tables comparing configurations
- ⭐ Best configuration marked with a star
- 🏆 Final recommendations
- 💡 Optimization suggestions

## After Testing

1. **Check the report**:
   ```bash
   cat test_results.json
   # or
   python -m json.tool test_results.json
   ```

2. **Review recommendations**:
   Look for "🏆 Recommended Configuration" section

3. **Update your production config**:
   Use the recommended number of draft tokens

4. **Compare different runs**:
   Save results with timestamps:
   ```bash
   cp test_results.json test_results_$(date +%Y%m%d_%H%M%S).json
   ```

## Troubleshooting

### "Speculative server is not running"
Start it first:
```bash
python test_speculative.py
```

### "Connection timeout"
- Check if server crashed (look at terminal where server is running)
- Verify no firewall blocking port 8000
- Restart the server

### "Import Error: rich"
Either:
- Install it: `pip install rich`
- Or ignore - script works without it (just less pretty)

### Slow Performance
- Close other applications
- Check GPU usage: `nvidia-smi` (if using GPU)
- Ensure models are loaded in memory

### Tests Failing
- Verify models are downloaded correctly
- Check available RAM/VRAM
- Review server logs for errors
- Try baseline test first (no speculative)

## Example Session

```bash
# Terminal 1: Start server
$ python test_speculative.py
Starting vLLM server...
Server started successfully

# Terminal 2: Run tests
$ python test_speculative_complete.py
Testing Speculative Decoding Setup
===================================

Server Status:
✅ Speculative (port 8000): RUNNING

Performance Tests:
------------------
Testing: No speculative decoding
✅   18.2 tokens/sec, 13.74s total

Testing: 3 draft tokens
✅   24.1 tokens/sec, 10.37s total

Testing: 5 draft tokens
✅   29.8 tokens/sec, 8.39s total

Testing: 7 draft tokens
✅   27.3 tokens/sec, 9.16s total

[... more output ...]

🏆 Recommended Configuration: 5 draft tokens
   Performance: 29.8 tokens/sec
   Speedup: +64% vs baseline

✨ Testing complete!
```

## Understanding Results

### Great Performance (50-70% speedup)
✅ Everything working optimally
✅ Use in production
✅ This is what you want!

### Good Performance (30-50% speedup)
✅ Working well
✅ Safe to use
✅ Minor optimization possible

### Poor Performance (0-30% speedup)
⚠️ Check configuration
⚠️ Try different draft model
⚠️ Verify GPU is being used

### Negative Performance (slower than baseline)
❌ Something wrong
❌ Check logs for errors
❌ Disable speculative for now

## Next Steps

1. ✅ Review `test_results.json`
2. ✅ Note the recommended configuration
3. ✅ Update your server startup with optimal settings
4. ✅ Test with your real workload
5. ✅ Monitor in production
6. ✅ Re-run tests periodically

## Files Created

- `test_results.json` - Full test results
- Test output in terminal

## Getting Help

1. Check `TESTING_GUIDE.md` for detailed explanations
2. Review `QUICK_REFERENCE.md` for quick tips
3. Look at `example_test_output.txt` for expected output
4. Compare with `example_test_results.json`

## Pro Tips

- 💡 Run tests after any configuration change
- 📊 Save results for historical comparison
- 🎯 Test with your actual prompts (modify script)
- ⚡ 5 draft tokens is usually optimal
- 🔄 Re-test after model updates

Happy testing! 🚀
