# 🎯 Model Use Cases & Recommendations

**For**: M4 Pro (16GB) + MLX-optimized models
**Last Updated**: 2026-02-09

---

## 🔐 Security & Pentesting Workflows

### CTF Challenges & Security Research
**Best Models**:
1. **Josiefied-Qwen3-8B-abliterated** - Uncensored, balanced performance
2. **WhiteRabbitNeo-Coder** - Specialized cybersecurity training
3. **Josiefied-Qwen3-14B-abliterated** - Most capable, use for complex research

**Why These?**
- Abliterated models have safety guardrails removed
- Will discuss exploitation techniques without refusal
- Ideal for authorized security testing scenarios

**Example Tasks**:
- Analyzing malware behavior
- Writing proof-of-concept exploits (authorized contexts)
- Security code review
- Vulnerability research
- CTF challenge solutions

**Workflow**:
```bash
# Quick security queries (fast iteration)
python3 test_model.py ./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit

# Complex security research (quality over speed)
python3 test_model.py ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit
```

---

## 💻 Software Development

### Quick Coding Assistant (Interactive)
**Best Model**: **Qwen3-4B-4bit**
- Speed: 47 tokens/s
- Fast enough for real-time suggestions
- Good code quality
- Low memory footprint

**Example Tasks**:
- Code completion and suggestions
- Bug fixes
- Refactoring suggestions
- Documentation generation

### Complex Code Analysis
**Best Models**:
1. **qwen3-7b** - Balanced analysis/generation
2. **mistral-7b** - Strong instruction following
3. **Josiefied-Qwen3-8B** - For unrestricted code patterns

**Example Tasks**:
- Architecture reviews
- Code quality analysis
- Complex refactoring
- Algorithm optimization

### Cybersecurity Code Review
**Best Model**: **WhiteRabbitNeo-Coder**
- Specialized for security-focused code analysis
- Trained on cybersecurity datasets
- Good at identifying vulnerabilities

**Example Tasks**:
- Finding SQL injection vectors
- Identifying XSS vulnerabilities
- Security-focused code review
- Threat modeling

---

## 🧠 Reasoning & Problem Solving

### Chain-of-Thought Reasoning
**Best Model**: **DeepSeek-R1-1.5B-3bit**
- Distilled from reasoning-focused model
- Fast inference (84 tokens/s)
- Explicit reasoning steps

**Example Tasks**:
- Math problems
- Logical puzzles
- Step-by-step analysis
- Decision making

### Complex Reasoning (Quality Focus)
**Best Model**: **Josiefied-Qwen3-14B-abliterated**
- Most capable model in collection
- Worth the slower speed for hard problems
- Uncensored (explores all solution paths)

**Example Tasks**:
- Complex security analysis
- Multi-step problem solving
- Research planning
- Strategic thinking

---

## 📚 Research & Learning

### Quick Information Lookup
**Best Models**:
1. **DeepSeek-R1-1.5B** (84 t/s) - Fast reasoning
2. **Josiefied-Qwen3-1.7B** (92 t/s) - Fastest overall
3. **Qwen3-4B** (47 t/s) - Better quality

**Workflow**:
- Use smallest model that answers your question
- Escalate to larger models if answer is insufficient
- 1.5B → 4B → 8B → 14B (quality progression)

### Deep Research
**Best Model**: **Josiefied-Qwen3-14B-abliterated**
- Most capable for complex topics
- Uncensored (explores controversial topics)
- Worth the wait for difficult questions

---

## 🎨 Creative & Unrestricted Tasks

### Unrestricted Text Generation
**Best Models** (all abliterated/uncensored):
1. **dolphin3-8b** - Highly uncensored, creative
2. **Josiefied-Qwen3-8B** - Balanced capability
3. **Josiefied-Qwen3-14B** - Most capable

**Example Tasks**:
- Exploring hypothetical scenarios
- Security scenario planning
- Unrestricted brainstorming
- Red team planning

**Note**: These models are specifically chosen for security research and authorized testing contexts.

---

## ⚡ Speed vs. Quality Trade-offs

### When Speed Matters (Interactive Use)
Pick from **Fast Tier** (30+ tokens/s after warmup):
- Josiefied-Qwen3-1.7B (92 t/s)
- DeepSeek-R1-1.5B (84 t/s)
- Qwen3-4B (47 t/s)
- mistral-7b (33 t/s)

**Use Cases**:
- Development workflow integration
- Quick queries during work
- Real-time suggestions
- Exploratory testing

### When Quality Matters (Batch/Research)
Pick from **Quality Tier** (slower but more capable):
- Josiefied-Qwen3-14B (most capable)
- Josiefied-Qwen3-8B (balanced)
- dolphin3-8b (creative)
- WhiteRabbitNeo-Coder (security specialist)

**Use Cases**:
- Complex security analysis
- Critical code reviews
- Research tasks
- Important decisions

---

## 🌍 Multilingual Tasks

### English + Chinese Support
**Best Model**: **qwen3-7b**
- Native Chinese language model
- Excellent English performance
- Good for bilingual codebases

**Example Tasks**:
- Translating documentation
- Working with Chinese APIs
- Bilingual code comments
- Cross-language research

---

## 🔧 Model Selection Flowchart

```
Need answer fast? (interactive use)
├─ YES → Use 1.7B or 1.5B models
│        (90+ tokens/s)
│
└─ NO → Need highest quality?
    ├─ YES → Use 14B model
    │        (0.8 t/s first run, faster after warmup)
    │
    └─ NO → Need uncensored?
        ├─ YES → Josiefied-8B or dolphin3-8b
        │
        └─ NO → Use Qwen3-4B or mistral-7b
                 (balanced performance)

Security-specific task?
└─ Use WhiteRabbitNeo-Coder or Josiefied models
```

---

## 💡 Pro Tips

### Warming Up Models
First generation after loading is slow (MLX compilation):
```bash
# Warm up with a short prompt
echo "Say hello" | python3 test_model.py ./mlx/MODEL_NAME

# Then use normally (much faster)
```

### Memory Management
- **24GB M4 Pro Tips**:
  - Run 2-3 models at a time comfortably
  - 14B model runs fine alongside other work (plenty of RAM!)
  - Smaller models (1-4B) can run 3-4 simultaneously

### Context Length Strategy
- **Short context (2K-4K)**: Fastest generation
- **Medium context (8K)**: Balanced (recommended)
- **Long context (16K+)**: Slower but handles complex tasks

### Parallel Workflows
Run multiple small models for different tasks:
```bash
# Terminal 1: Fast reasoning
python3 test_model.py ./mlx/DeepSeek-R1-1.5B-3bit

# Terminal 2: Fast coding
python3 test_model.py ./mlx/Qwen3-4B-4bit

# Both run smoothly on 24GB M4 Pro
```

---

## 📊 Benchmark Comparison

| Use Case | Best Model | Speed | Quality | Memory |
|----------|-----------|-------|---------|--------|
| Quick queries | Josiefied-1.7B | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | 0.9GB |
| Fast reasoning | DeepSeek-R1-1.5B | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 0.7GB |
| Coding | Qwen3-4B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 2.0GB |
| Security | WhiteRabbitNeo | ⚡⚡⚡ | ⭐⭐⭐⭐ | 4.0GB |
| Uncensored 8B | Josiefied-8B | ⚡⚡ | ⭐⭐⭐⭐⭐ | 4.3GB |
| Best quality | Josiefied-14B | ⚡ | ⭐⭐⭐⭐⭐ | 14GB |

---

## 🚀 Quick Start Examples

### Security Research Session
```bash
cd /Users/jonathanmallinger/models
source .venv/bin/activate

# Start with fast model for exploration
python3 test_model.py ./mlx/Josiefied-Qwen3-1.7B-abliterated-v1-4bit
# Prompt: "Explain SQL injection basics"

# Switch to specialist for deep analysis
python3 test_model.py ./mlx/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-mlx
# Prompt: "Analyze this code for SQL injection: [paste code]"
```

### Development Workflow
```bash
# Keep fast model running for quick questions
python3 test_model.py ./mlx/Qwen3-4B-4bit
# Quick coding questions during development

# Use larger model for complex refactoring
python3 test_model.py ./mlx/qwen3-7b
# Complex architecture decisions
```

### Research & Analysis
```bash
# Start with reasoning model
python3 test_model.py ./mlx/DeepSeek-R1-Distill-Qwen-1.5B-3bit
# Quick analysis and step-by-step thinking

# Escalate to 14B for hard problems
python3 test_model.py ./mlx/Josiefied-Qwen3-14B-abliterated-v3-6bit
# Complex multi-step analysis
```

---

## ⚠️ Important Notes

### Abliterated Models
- "Abliterated" = Safety guardrails removed
- Use responsibly in authorized contexts only
- Ideal for security research, not production
- Will discuss techniques censored models refuse

### WhiteRabbitNeo Specifics
- Trained on cybersecurity datasets
- Specialized knowledge of security concepts
- More accurate for vulnerability analysis
- Use for pentesting and CTF work

### First Run Performance
- All models slow on first generation (MLX compilation)
- Second generation is 5-10x faster
- Warm up models with test prompt before serious use

---

**Remember**: The best model depends on your specific task. Start small and fast, escalate to larger models only when needed.
