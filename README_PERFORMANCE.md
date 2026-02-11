# Performance Comparison - Quick Reference

## TL;DR

**For OpenCode Integration: Use LM Studio CLI**
- 68% faster (22.9 vs 13.6 tok/s)
- OpenAI-compatible API
- 226ms time to first token
- Easy setup

**Trade-off:** Some stability issues (60% vs 100% reliability)

---

## Quick Stats

| Metric | Direct MLX | LM Studio |
|--------|------------|-----------|
| Speed | 13.6 tok/s | 22.9 tok/s |
| Reliability | 100% | 60% |
| TTFT | N/A | 226ms |
| Memory | 4.35 GB | ~4-5 GB |
| API | No | Yes |

---

## Files Generated

1. **FINAL_PERFORMANCE_TABLE.md** (12K) - Executive summary
2. **PERFORMANCE_COMPARISON_REPORT.md** (11K) - Full analysis
3. **QUICK_COMPARISON.md** (6.9K) - Quick reference
4. **server_comparison_results.json** (6.5K) - LM Studio data
5. **direct_mlx_benchmark.json** (6.0K) - Direct MLX data
6. **server_performance_comparison.py** (17K) - Benchmark script
7. **direct_mlx_benchmark.py** (3.7K) - MLX test script

---

## OpenCode Setup

```json
{
  "provider": "openai",
  "baseURL": "http://localhost:1234/v1",
  "model": "josiefied-qwen3-8b-abliterated-v1"
}
```

---

## Test Results

### Direct MLX-LM
- SQL Injection: 10.8 tok/s ✓
- XSS: 16.6 tok/s ✓
- CSRF: 10.9 tok/s ✓
- Buffer Overflow: 16.2 tok/s ✓
- **Success: 4/4 (100%)**

### LM Studio CLI
- SQL Injection: 39.2 tok/s ✓
- XSS: CRASHED ✗
- CSRF: CRASHED ✗
- Buffer Overflow: 8.6/20.9 tok/s ✓
- **Success: 3/5 (60%)**

---

## Recommendation

Use **LM Studio CLI** for OpenCode - the speed improvement (68%) outweighs the reliability concerns for interactive development. Keep Direct MLX as backup for critical batch operations.
