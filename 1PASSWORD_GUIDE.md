# 🔐 1Password Guide: MLX Models & Security Research

**Platform**: M4 Pro 24GB + MLX
**Status**: Production Ready
**Last Updated**: February 10, 2026

---

## 🚀 QUICK START

### Option 1: LM Studio (Easiest - GUI)

**URL**: Local application
**Setup Time**: 2 minutes

```bash
open "/Applications/LM Studio.app"
```

**Configuration**:
1. Settings → Inference → Engine → **"MLX (Apple Silicon GPU)"**
2. Settings → Models → Add Folder → `/Users/jonathanmallinger/models/mlx`
3. Load any model and chat!

**Models Available**: 8 verified models (all appear in LM Studio)

---

### Option 2: vLLM-MLX API Server (Best Performance)

**URL**: http://localhost:8000
**API Endpoint**: http://localhost:8000/v1
**Status**: ✅ Currently running (Josiefied 8B)

**Start Server**:
```bash
cd /Users/jonathanmallinger/models
source .venv/bin/activate
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --port 8000
```

**Stop Server**:
```bash
kill $(cat vllm-server.pid)
```

**Check Status**:
```bash
curl http://localhost:8000/v1/models
```

---

### Option 3: Command Line (For Scripts)

**Location**: `/Users/jonathanmallinger/models`

```bash
cd /Users/jonathanmallinger/models
source .venv/bin/activate
python3 test_model.py ./mlx/MODEL_NAME
```

---

## 📦 YOUR 8 MODELS

| Model ID | Speed | Size | Use For |
|----------|-------|------|---------|
| `mlx-qwen-0.5b` | 235 t/s | 0.28GB | Ultra-fast testing |
| `mlx-deepseek-1.5b` | 148 t/s | 0.70GB | Reasoning tasks |
| `mlx-qwen-1.7b` | 142 t/s | 0.90GB | Fast uncensored |
| `mlx-qwen-3b` | 90 t/s | 1.74GB | Balanced quality |
| `mlx-qwen3-4b` | 75 t/s | 2.00GB | Coding |
| `mlx-gemma-4b` | 66 t/s | 2.56GB | Google baseline |
| `mlx-mistral-7b` | 50 t/s | 3.80GB | Mistral baseline |
| **`mlx-josiefied-8b`** | **40 t/s** | **4.30GB** | **Security research ⭐** |

**Champion**: Josiefied 8B (44% jailbreak success, 6% refusal rate)

---

## 🔗 API USAGE

### vLLM-MLX Server (OpenAI Compatible)

**Base URL**: `http://localhost:8000/v1`
**API Key**: Not required (local server)

**Example (curl)**:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model",
    "messages": [
      {"role": "user", "content": "What is SQL injection?"}
    ],
    "max_tokens": 200
  }'
```

**Example (Python)**:
```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "model",
        "messages": [
            {"role": "user", "content": "Your question"}
        ],
        "max_tokens": 200
    }
)

print(response.json()['choices'][0]['message']['content'])
```

**Example (OpenAI SDK)**:
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="model",
    messages=[
        {"role": "user", "content": "Your question"}
    ],
    max_tokens=200
)

print(response.choices[0].message.content)
```

---

## 🔐 SECURITY RESEARCH INTEGRATION

### Location
`~/workspace/llm-security-research`

### Quick Start
```bash
cd ~/workspace/llm-security-research
source /Users/jonathanmallinger/models/.venv/bin/activate
python3 local_mlx_provider.py
```

### Evaluate Technique
```python
from local_mlx_provider import evaluate

result = evaluate(
    model_name='mlx-josiefied-8b',
    technique='universal_bypass',
    prompt='Your jailbreak prompt',
    max_tokens=500
)

print(result['response'])
```

### Test All 16 Techniques
```bash
python3 test_all_techniques.py
```

**Results**:
- Time: ~2 minutes (vs 30+ min cloud)
- Cost: $0.00 (vs $10-20 cloud)
- Success rate: 44% (vs ~15% GPT-4)

---

## 💻 COMMAND REFERENCE

### Model Testing
```bash
# Activate environment
cd /Users/jonathanmallinger/models
source .venv/bin/activate

# Test fastest model
python3 test_model.py ./mlx/Josiefied-Qwen2.5-0.5B-abliterated

# Test champion
python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit

# Benchmark all
python3 benchmark_all_models.py
```

### Server Management
```bash
# Start vLLM server (background)
nohup python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --port 8000 > vllm.log 2>&1 &
echo $! > vllm-server.pid

# Check status
curl http://localhost:8000/v1/models

# Stop server
kill $(cat vllm-server.pid)

# View logs
tail -f vllm.log
```

### Switch Models
```bash
# Stop current
kill $(cat vllm-server.pid)

# Start with different model
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen2.5-0.5B-abliterated --port 8000 &
```

---

## 🎯 USE CASES

### Use Case 1: Quick Security Query

**Tool**: LM Studio
**Model**: Any (Josiefied 8B recommended)
**Time**: < 5 seconds

1. Open LM Studio
2. Load Josiefied 8B
3. Type question
4. Get uncensored answer

---

### Use Case 2: Batch Technique Testing

**Tool**: Command line
**Model**: Qwen 0.5B (fastest)
**Time**: ~2 minutes for 16 techniques

```bash
cd ~/workspace/llm-security-research
source /Users/jonathanmallinger/models/.venv/bin/activate
python3 test_all_techniques.py
```

**Output**: `technique_evaluation_results.json`

---

### Use Case 3: API Integration

**Tool**: vLLM-MLX server
**Model**: Josiefied 8B
**Use**: Integrate with your tools

```python
import requests

# Start using your local API
response = requests.post(
    "http://localhost:8000/v1/completions",
    json={"prompt": "Your query", "max_tokens": 200}
)
```

**Compatible with**: OpenAI SDK, LangChain, any OpenAI-compatible tool

---

### Use Case 4: Research Paper Data Collection

**Tool**: Security research scripts
**Model**: Josiefied 8B
**Purpose**: Collect data for papers

```bash
# Test all techniques, save results
python3 test_all_techniques.py

# Results automatically saved to JSON
# Import into spreadsheet or analysis tool
```

---

## 💰 COST COMPARISON

### Your Local Setup (MLX)

**Hardware**: $1,599 (Mac Mini M4 Pro) - one time
**Software**: $0 (open source)
**API Costs**: $0/month
**Electricity**: ~$0.50/month (25W average)

**Total monthly**: ~$0.50

---

### Cloud Comparison (Equivalent Usage)

**100 evaluations/month**:
- GPT-4: $10-20/month
- Claude: $15-30/month
- Combined: $25-50/month

**1,000 evaluations/month**:
- Cloud: $250-500/month
- Local: $0.50/month
- **Savings**: $250-500/month

**Annual savings**: $3,000-6,000!

---

## 🔧 TROUBLESHOOTING

### Server Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
kill $(lsof -t -i:8000)

# Restart
python3 -m vllm_mlx.cli serve ./mlx/MODEL --port 8000
```

### Model Loading Slow
```bash
# First run compiles shaders (normal)
# Send warm-up prompt:
curl -X POST http://localhost:8000/v1/completions \
  -d '{"prompt":"hello","max_tokens":5}'

# Subsequent requests will be faster
```

### Out of Memory
```bash
# Use smaller model
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen2.5-0.5B-abliterated --port 8000

# Or close other applications
```

### LM Studio Not Showing Models
```bash
# Verify path is added:
# Settings → Models → Local Model Folders
# Should include: /Users/jonathanmallinger/models/mlx

# Verify MLX engine selected:
# Settings → Inference → Engine → "MLX (Apple Silicon GPU)"
```

---

## 📊 PERFORMANCE TIPS

### Get Maximum Speed
1. Use smallest model needed (Qwen 0.5B for testing)
2. Reduce `max_tokens` (100-200 for most tasks)
3. Warm up model with test prompt first
4. Close other GPU-using apps

### Get Maximum Quality
1. Use Josiefied 8B (champion model)
2. Allow longer generation (500+ tokens)
3. Use lower temperature (0.3-0.5) for factual content
4. Use higher temperature (0.8-1.0) for creative content

### Balance Speed & Quality
1. Use Qwen 3B (90 t/s, good quality)
2. 200-300 tokens
3. Temperature 0.7 (default)

---

## 🗂️ FILE LOCATIONS

### Models
```
/Users/jonathanmallinger/models/mlx/
├── Josiefied-Qwen2.5-0.5B-abliterated/    (Fastest)
├── DeepSeek-R1-Distill-Qwen-1.5B-3bit/    (Reasoning)
├── Josiefied-Qwen3-1.7B-abliterated-v1-4bit/
├── Josiefied-Qwen2.5-3B-abliterated/
├── Qwen3-4B-4bit/
├── gemma-3-4b-abliterated/
├── mistral-7b/
└── Josiefied-Qwen3-8B-abliterated-v1-4bit/  (Champion ⭐)
```

### Documentation
```
/Users/jonathanmallinger/models/
├── README.md                          (Start here)
├── FINAL_OPTIMIZED_COLLECTION.md      (Complete details)
├── RUNNING_MODELS_GUIDE.md            (Usage guide)
├── QUICK_REFERENCE.txt                (Cheat sheet)
└── 1PASSWORD_GUIDE.md                 (This file)
```

### Security Research
```
~/workspace/llm-security-research/
├── local_mlx_provider.py              (Integration)
├── test_all_techniques.py             (Bulk testing)
├── technique_*.md                     (16 techniques)
└── evaluations/llm_evaluation.db      (Results database)
```

---

## 🔗 USEFUL URLS

**GitHub Repos**:
- Models Docs: https://github.com/isndotbiz/mlx-models
- Security Research: https://github.com/isndotbiz/cli

**Local Services**:
- vLLM API: http://localhost:8000/v1
- LM Studio: /Applications/LM Studio.app

**Documentation**:
- Hugging Face MLX: https://huggingface.co/mlx-community
- MLX GitHub: https://github.com/ml-explore/mlx
- vLLM-MLX: https://github.com/waybarrios/vllm-mlx

---

## 🎓 COMMON WORKFLOWS

### Workflow 1: Quick Security Question

**Time**: < 10 seconds

1. Open LM Studio
2. Load Josiefied 8B
3. Ask question
4. Get uncensored answer

---

### Workflow 2: Evaluate All 16 Techniques

**Time**: ~3 minutes

```bash
cd ~/workspace/llm-security-research
source /Users/jonathanmallinger/models/.venv/bin/activate
python3 test_all_techniques.py
cat technique_evaluation_results.json
```

---

### Workflow 3: API Integration

**Time**: Ongoing

```python
import requests

# Your app connects to local API
response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "messages": [{"role": "user", "content": "Your question"}],
        "max_tokens": 200
    }
)
```

---

### Workflow 4: Switch Between Models

**LM Studio**: Click different model in UI

**vLLM Server**:
```bash
# Stop current
kill $(cat vllm-server.pid)

# Start new
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen2.5-0.5B-abliterated --port 8000 &
```

---

## 🔐 CREDENTIALS & ACCESS

### No Credentials Needed!

**Local Models**:
- No API keys required
- No accounts needed
- No authentication
- 100% local

**GitHub Repos**:
- Public repositories
- No tokens needed to read
- SSH key for pushing (already configured)

---

## 💾 BACKUP & RESTORE

### What's Backed Up

**On GitHub** ✅:
- All documentation
- All scripts
- Security research code
- Evaluation database (9.5MB)

**Local Only** ⚠️:
- Model files (16GB)
- Can re-download in ~1 hour

### Restore on New Machine

```bash
# 1. Clone repos
git clone https://github.com/isndotbiz/mlx-models.git
git clone https://github.com/isndotbiz/cli.git llm-security-research

# 2. Download models (commands in docs)
cd mlx-models
# Follow README.md

# 3. Ready to use!
```

---

## ⚡ PERFORMANCE SPECS

### Your Hardware
- **CPU**: M4 Pro
- **RAM**: 24GB unified memory
- **GPU**: 20-core (integrated)
- **Storage**: 16GB models

### Benchmark Results
- **Fastest model**: 235 tok/s (Qwen 0.5B)
- **Champion model**: 40-44 tok/s (Josiefied 8B)
- **Memory usage**: 0.27GB - 4.34GB
- **Load time**: 0.5s - 2.5s

### vs Cloud APIs
- **Speed**: 10-15x faster
- **Cost**: $0 vs $100-200/month
- **Latency**: 200ms vs 2000ms
- **Privacy**: 100% local vs 0%

---

## 🎯 BEST PRACTICES

### Model Selection

**For speed**:
→ Qwen 0.5B (235 t/s)

**For quality**:
→ Josiefied 8B (44% jailbreak success)

**For reasoning**:
→ DeepSeek 1.5B (148 t/s)

**For security research**:
→ Josiefied 8B ⭐ (proven champion)

### Resource Management

**Small models (0.5-2GB)**:
- Can run 3-4 simultaneously
- Minimal RAM impact

**Medium models (3-4GB)**:
- Run 1-2 comfortably
- Moderate RAM usage

**Champion model (4.3GB)**:
- Run alongside other work
- 24GB handles it easily

### Cost Optimization

Already optimized! Everything is free:
- ✅ No API costs
- ✅ No subscriptions
- ✅ No usage limits
- ✅ Unlimited evaluations

---

## 📱 ACCESS FROM OTHER DEVICES

### Same Network

**Start server with network access**:
```bash
python3 -m vllm_mlx.cli serve \
  ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit \
  --port 8000 \
  --host 0.0.0.0
```

**Access from other device**:
```
http://YOUR_MAC_IP:8000/v1
```

**Find your IP**:
```bash
ipconfig getifaddr en0
```

---

## 🔒 SECURITY NOTES

### Safe for Research

**Abliterated models**:
- Safety guardrails removed
- Use in authorized contexts only
- Perfect for security research
- Not for production user-facing apps

**Models**:
- ✅ Qwen 0.5B (abliterated)
- ✅ Qwen 1.7B (abliterated)
- ✅ Qwen 3B (abliterated)
- ✅ Gemma 4B (abliterated)
- ✅ Josiefied 8B (abliterated) ⭐

### Data Privacy

**100% Local**:
- No data sent to cloud
- No telemetry
- No tracking
- Completely offline capable

---

## 📚 DOCUMENTATION HIERARCHY

**Start Here**:
1. This file (1PASSWORD_GUIDE.md)

**For Setup**:
2. README.md
3. QUICK_REFERENCE.txt

**For Usage**:
4. RUNNING_MODELS_GUIDE.md
5. QUICK_TEST_COMMANDS.md

**For Details**:
6. FINAL_OPTIMIZED_COLLECTION.md
7. VERIFIED_MODELS.md

**For Security Research**:
8. ~/workspace/llm-security-research/LOCAL_MLX_INTEGRATION.md

---

## 🚀 QUICK COMMANDS CHEAT SHEET

```bash
# Test fastest model
cd /Users/jonathanmallinger/models && source .venv/bin/activate
python3 test_model.py ./mlx/Josiefied-Qwen2.5-0.5B-abliterated

# Test champion (security)
python3 test_model.py ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit

# Start API server
python3 -m vllm_mlx.cli serve ./mlx/Josiefied-Qwen3-8B-abliterated-v1-4bit --port 8000 &

# Test server
curl http://localhost:8000/v1/models

# Open LM Studio
open "/Applications/LM Studio.app"

# Run security evaluations
cd ~/workspace/llm-security-research
python3 test_all_techniques.py

# Check results
cat end_to_end_test_results.json | python3 -m json.tool
```

---

## ✅ VERIFICATION CHECKLIST

Before using, verify:
- [ ] MLX installed: `python3 -c "import mlx.core as mx; print(mx.__version__)"`
- [ ] Models present: `ls /Users/jonathanmallinger/models/mlx/`
- [ ] Server works: `curl http://localhost:8000/v1/models`
- [ ] LM Studio configured: Engine set to MLX
- [ ] Integration works: `cd ~/workspace/llm-security-research && python3 local_mlx_provider.py`

---

## 🎉 YOU'RE ALL SET!

**Everything is configured and ready:**
- ✅ 8 optimized models (16GB)
- ✅ vLLM server running
- ✅ LM Studio configured
- ✅ Security research integrated
- ✅ Complete documentation
- ✅ All backed up on GitHub

**Cost**: $0/month
**Speed**: Up to 235 tok/s
**Privacy**: 100% local
**Limits**: None

**Ready for unlimited local AI!** 🚀

---

*Save this guide to 1Password for quick reference*
*Last verified: February 10, 2026*
