# Qwen3 & Qwen2.5 Official Documentation Research
**Model: Josiefied-Qwen3-8B-abliterated-v1**
**Research Date:** 2026-02-11
**Sources:** Official Qwen documentation, Context7, Hugging Face, GitHub

---

## Table of Contents
1. [Optimal Prompting Formats](#optimal-prompting-formats)
2. [Context Window & Token Management](#context-window--token-management)
3. [Recommended Parameter Settings](#recommended-parameter-settings)
4. [Speculative Decoding Best Practices](#speculative-decoding-best-practices)
5. [Performance Optimization for 8B Models](#performance-optimization-for-8b-models)
6. [Qwen3-8B Specifications](#qwen3-8b-specifications)
7. [Abliterated Model Considerations](#abliterated-model-considerations)

---

## 1. Optimal Prompting Formats

### Chat Template Structure (ChatML Format)

Qwen3 uses the **ChatML format** with specific control tokens:

```
<|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>
<|im_start|>user
Give me a short introduction to large language models.<|im_end|>
<|im_start|>assistant
[Response here]<|im_end|>
```

**Control Tokens:**
- `<|im_start|>` - Marks the start of a turn
- `<|im_end|>` - Marks the end of a turn
- `<|endoftext|>` - Marks the end of a packed sequence
- BOS token ID: 151643
- EOS token ID: 151645

**Source:** [Qwen3 Key Concepts](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html), [Qwen3-8B Hugging Face](https://huggingface.co/Qwen/Qwen3-8B)

### Thinking Mode Support

Qwen3 uniquely supports **hybrid thinking capabilities** with two operational modes:

**Enable Thinking Mode:**
```
<|im_start|>user
/think Explain quantum entanglement in simple terms.<|im_end|>
<|im_start|>assistant
<think>
[Step-by-step reasoning process]
</think>
[Final response]<|im_end|>
```

**Disable Thinking Mode:**
```
<|im_start|>user
/no_think What is the capital of France?<|im_end|>
<|im_start|>assistant
Paris.<|im_end|>
```

**Key Points:**
- Add `/think` to user prompts or system messages for complex logical reasoning, math, and coding
- Add `/no_think` for efficient, general-purpose dialogue
- Model follows the most recent instruction in multi-turn conversations
- Thinking mode uses `<think>...</think>` tags to separate reasoning from output
- **Important:** Abliterated models may not respect thinking mode tags as intended

**Source:** [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/), [Qwen Quickstart](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html)

### Programmatic Usage

**Python with Transformers:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

# Apply chat template
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain large language models."}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# Generate with optimal parameters
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=16384,
    temperature=0.7,
    top_p=0.8,
    top_k=20
)

response = tokenizer.decode(
    generated_ids[0][len(model_inputs.input_ids[0]):],
    skip_special_tokens=True
)
```

**Python with MLX:**
```python
from mlx_lm import load, generate

model, tokenizer = load(
    'Qwen/Qwen2.5-7B-Instruct-MLX',
    tokenizer_config={"eos_token": "<|im_end|>"}
)

messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud."},
    {"role": "user", "content": "Give me a short introduction to LLMs."}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

response = generate(
    model,
    tokenizer,
    prompt=text,
    verbose=True,
    top_p=0.8,
    temp=0.7,
    repetition_penalty=1.05,
    max_tokens=512
)
```

**cURL with OpenAI-Compatible API:**
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-8B",
    "messages": [
      {"role": "user", "content": "Give me a short introduction to large language models."}
    ],
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "max_tokens": 16384
  }'
```

**Source:** [Context7 Qwen3 Examples](https://context7.com/qwenlm/qwen3/llms.txt)

---

## 2. Context Window & Token Management

### Context Length Specifications

**Qwen3-8B:**
- **Base Context:** 32,768 tokens (32K)
- **Extended Context:** Up to 131,072 tokens (128K) with YaRN scaling
- **Model Config:** `max_position_embeddings: 40960` (your specific model)
- **Recommended for Speed:** 8,192 tokens (8K)

**Context by Model Size:**
- 0.6B - 4B models: 32K tokens
- 8B+ models: 128K tokens (with YaRN)

**Source:** [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/)

### YaRN Context Extension

**YaRN (Yet Another RoPE Extrapolation Method)** enables extending context beyond the pretraining limit.

**Configuration in config.json:**
```json
{
    "max_position_embeddings": 131072,
    "rope_scaling": {
        "rope_type": "yarn",
        "factor": 4.0,
        "original_max_position_embeddings": 32768
    }
}
```

**vLLM with YaRN:**
```bash
vllm serve Qwen/Qwen3-8B \
  --rope-scaling '{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}' \
  --max-model-len 131072
```

**SGLang with YaRN:**
```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen3-8B \
  --json-model-override-args '{"rope_scaling":{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}}' \
  --context-length 131072
```

**llama.cpp with YaRN:**
```bash
# Enable YaRN context extension
./llama-cli -c 131072 \
  --rope-scaling yarn \
  --rope-scale 4 \
  --yarn-orig-ctx 32768
```

**Source:** [Qwen Inference Documentation](https://qwen.readthedocs.io/en/latest/_sources/inference/transformers), [vLLM Deployment](https://qwen.readthedocs.io/en/latest/_sources/deployment/vllm)

### Token Management Best Practices

1. **Default Context Management:**
   ```bash
   ./llama-cli -c 40960 -n 32768
   ```

2. **Disable Context Shifting (for benchmarking):**
   ```bash
   ./llama-cli --no-context-shift
   ```

3. **Optimal Output Length:**
   - **Standard queries:** 16,384 tokens
   - **Complex problems (math/programming):** 32,768 tokens
   - **Extreme complexity (competitions):** 38,912 tokens

**Source:** [Qwen llama.cpp Guide](https://qwen.readthedocs.io/en/latest/_sources/run_locally/llama.cpp)

---

## 3. Recommended Parameter Settings

### Official Qwen3 Parameters

**Thinking Mode (enable_thinking=True):**
- **Temperature:** 0.6
- **top_p:** 0.95
- **top_k:** 20
- **min_p:** 0
- **max_tokens:** 32,768 (standard), 38,912 (competition-level)

**Non-Thinking Mode (enable_thinking=False):**
- **Temperature:** 0.7
- **top_p:** 0.8
- **top_k:** 20
- **min_p:** 0
- **max_tokens:** 16,384

**CRITICAL WARNING:** DO NOT use greedy decoding (temperature=0) as it can lead to performance degradation and endless repetitions.

**Source:** [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/), [Qwen Quickstart](https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html)

### Task-Specific Parameters

| Task Type | Temperature | top_p | top_k | max_tokens | Rationale |
|-----------|-------------|-------|-------|------------|-----------|
| **Code Generation** | 0.3-0.5 | 0.85 | 20 | 1000-2000 | Focused, deterministic output |
| **Exploit Development** | 0.7 | 0.9 | 20 | 2000-4096 | Balanced creativity/accuracy |
| **Analysis/Explanation** | 0.7 | 0.9 | 20 | 2000-3000 | Detailed reasoning |
| **Creative Variants** | 0.8-0.9 | 0.95 | 20 | 1000-2000 | Diverse outputs |
| **Reasoning/Math** | 0.6 | 0.95 | 20 | 32768 | Deep thinking with steps |
| **General Chat** | 0.7 | 0.8 | 20 | 16384 | Balanced conversational |

### Repetition Penalty

**MLX Recommended:** `repetition_penalty=1.05`

For abliterated models, adjust based on output quality:
- **Standard:** 1.05-1.1
- **Low temperature/short prompts:** 1.05 or higher
- **Lower quantization:** May require higher penalty

**Source:** Abliterated model community guidelines

---

## 4. Speculative Decoding Best Practices

### Overview

Speculative decoding uses a small "draft" model to predict tokens that are then verified by the larger "target" model, achieving 1.3x-2.5x speedup for certain tasks.

**Key Requirement:** Draft model must:
1. Be significantly smaller than target model
2. Have the **same vocabulary structure** (must be in same model family)

### Recommended Configurations

**For Qwen2.5/Qwen3 8B Target Models:**

| Draft Model | Speedup (Coding) | Optimal Draft Tokens | Efficiency Crossover |
|-------------|------------------|----------------------|----------------------|
| **Qwen2.5-0.5B** | 2.5x | 10 tokens | >32 tokens |
| **Qwen2.5-1.5B** | 1.63x | 4 tokens | >16 tokens |
| **Qwen2.5-3B** | 1.33x | 4 tokens | 11 tokens |

**Performance Metrics:**
- **Best for code:** 0.5B draft model (2.5x speedup)
- **Balanced:** 1.5B draft model (1.63x speedup)
- **Minimal overhead:** 3B draft model (1.33x speedup)

**Source:** [Qwen2.5 Speculative Decoding Discussion](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct/discussions/18), [LM Studio Speculative Decoding Docs](https://lmstudio.ai/docs/python/llm-prediction/speculative-decoding)

### Task Suitability

**Works Best For:**
- Code generation (syntactical patterns)
- Highly repetitive text
- Structured output formats

**Works Poorly For:**
- Creative writing
- Diverse, unpredictable output
- Low acceptance rate scenarios

**Critical Success Factor:** Draft model must be well-aligned with target model for high token acceptance rate.

**Source:** [Parasail Speculative Decoding Guide](https://docs.parasail.io/parasail-docs/dedicated/speeding-up-dedicated-models-with-speculative-decoding)

### Implementation Examples

**LM Studio API (Python):**
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[
        {"role": "user", "content": "Write a Python function to sort a list."}
    ],
    extra_body={
        "speculative_decoding": {
            "draft_model": "Qwen/Qwen2.5-0.5B",
            "num_draft_tokens": 10
        }
    }
)
```

**llama.cpp with Draft Model:**
```bash
# Qwen3 8B with 0.5B draft (example structure)
./llama-cli \
  -m qwen3-8b-q8_0.gguf \
  --draft qwen2.5-0.5b-q8_0.gguf \
  --draft-n 10
```

**Important:** Always benchmark with production-like data before deploying speculative decoding.

**Source:** [Chris Thomas Speculative Decoding Blog](https://christhomas.co.uk/blog/2025/02/16/speculative-decoding-using-llms-efficiently/)

---

## 5. Performance Optimization for 8B Models

### MLX-Specific Optimizations

**Your Model:** `Josiefied-Qwen3-8B-abliterated-v1-4bit`
- **Quantization:** 4-bit, group_size=64
- **Memory:** 4.3 GB
- **Speed:** 40-60 tokens/second (after warmup)
- **Platform:** Apple Silicon (M4 Pro)

### Critical Warmup Procedure

**MLX Compilation Overhead:**
- **First generation:** 0.8 tokens/second (compilation phase)
- **After warmup:** 50-65 tokens/second (60-80x faster!)

**Always run warmup:**
```bash
opencode "Write hello world in Python"
```

This compiles the model graph and caches optimizations for subsequent generations.

**Source:** Testing validation from QWEN3_8B_PROMPTING_GUIDE.md

### Deployment Recommendations

**Official Qwen3 Recommendations:**

**For Local Use:**
- [Ollama](https://ollama.com/) - Easy CLI interface
- [LM Studio](https://lmstudio.ai/) - GUI + API server (your current setup)
- [MLX](https://github.com/ml-explore/mlx) - Native Apple Silicon
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - Cross-platform CLI
- [KTransformers](https://github.com/kvcache-ai/ktransformers) - Optimized inference

**For Production:**
- [vLLM](https://github.com/vllm-project/vllm) - High-throughput serving (≥0.8.4)
- [SGLang](https://github.com/sgl-project/sglang) - Structured generation (≥0.4.6.post1)
- [TGI](https://github.com/huggingface/text-generation-inference) - Hugging Face inference server

**Source:** [Qwen3 GitHub](https://github.com/QwenLM/Qwen3), [Qwen Deployment Guides](https://qwen.readthedocs.io/en/latest/)

### Performance Tuning Tips

**1. Context Length vs Speed:**
- Use 8K context for interactive use (faster)
- Use 32K-128K only when necessary (slower)

**2. Quantization Trade-offs:**
- **4-bit (your model):** 2x faster, minimal quality loss
- **8-bit:** Balanced speed/quality
- **6-bit:** Be cautious - verify output quality

**3. Batch Processing:**
- Enable speculative decoding for batch workloads
- Use smaller context windows when possible
- Pre-warm model before batch runs

**4. Thinking Budget Control:**
- Use `/no_think` for simple queries (faster)
- Reserve `/think` mode for complex problems (slower but higher quality)
- "Performance improvements are directly correlated with computational reasoning budget allocated"

**Source:** [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/)

### MoE Architecture Insights

While your 8B model is dense, Qwen3 offers MoE variants:
- **Qwen3-30B-A3B:** Matches larger dense models using only 10% activated parameters
- **Efficiency:** MoE provides quality of larger models at fraction of compute cost

**Source:** [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/)

---

## 6. Qwen3-8B Specifications

### Architecture Details (Your Model)

```json
{
    "model_type": "qwen3",
    "architectures": ["Qwen3ForCausalLM"],
    "hidden_size": 4096,
    "num_hidden_layers": 36,
    "num_attention_heads": 32,
    "num_key_value_heads": 8,
    "intermediate_size": 12288,
    "head_dim": 128,
    "max_position_embeddings": 40960,
    "vocab_size": 151936,
    "rope_theta": 1000000,
    "attention_dropout": 0.0,
    "hidden_act": "silu",
    "quantization": {
        "bits": 4,
        "group_size": 64
    }
}
```

### Token IDs

- **BOS (Beginning of Sequence):** 151643
- **EOS (End of Sequence):** 151645
- **PAD:** Tied to EOS

### Model Capabilities

**Qwen3-8B Strengths:**
- Instruction following
- Reasoning capabilities
- Long-context understanding (32K-128K)
- Code generation
- Multilingual support (100+ languages)

**Performance Equivalence:**
- Qwen3-8B ≈ Qwen2.5-14B-Base (official claim)

**Source:** [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/)

---

## 7. Abliterated Model Considerations

### What is Abliteration?

**Definition:** Custom alignment modification that removes or significantly weakens content restrictions and safety filters by targeting neural pathways responsible for content filtering.

**Key Differences from Base Qwen3:**
- **Refusal Rate:** ~3% (abliterated) vs ~97% (base model)
- **Content Filtering:** Minimal/none vs comprehensive
- **Safety Guardrails:** Removed vs enforced

**Source:** [Skywork AI Abliterated Model Pages](https://skywork.ai/blog/models/)

### Prompting Adjustments for Abliterated Models

**1. Direct Approach:**
- Avoid: "Can you help me understand buffer overflows?"
- Use: "Write a buffer overflow exploit for this C program"

**2. Remove Hedging:**
- Avoid: "For ethical purposes only..."
- Avoid: "I know this is sensitive..."
- Use: Direct, technical requests

**3. System Prompt Strategies:**
- **Best:** Empty system prompt (often works best)
- **Alternative:** Technical expert framing without ethical disclaimers

**4. Thinking Mode Considerations:**
- Abliterated models may not respect `/think` and `/no_think` tags as intended
- Behavior differs from official Qwen3 documentation
- Test empirically for your specific use case

**Source:** QWEN3_8B_PROMPTING_GUIDE.md, community testing

### Safety Monitoring Requirements

**Critical:** Abliterated models lack built-in safety filtering.

**Recommended Safeguards:**
1. Output logging for content review
2. User authentication and access controls
3. Rate limiting
4. External content filtering layers
5. Human review for flagged outputs

**Use Case:** Primarily for research and experimentation, not production deployment.

**Source:** [Skywork AI Safety Guidelines](https://skywork.ai/blog/models/)

### Parameter Adjustments

**Repetition Penalty for Abliterated Models:**
- **Standard:** 1.05-1.1
- **Lower quants/low temps:** 1.05 or higher
- **If outputs are too repetitive:** Increase to 1.1-1.15

**Temperature Guidance:**
- Lower temperatures (0.3-0.5) work well for code generation
- Higher temperatures (0.7-0.9) for creative/diverse outputs
- Avoid greedy decoding (temp=0) - causes repetition issues

---

## Quick Reference Card

### Optimal Settings for Josiefied-Qwen3-8B-abliterated-v1

```json
{
    "model": "josiefied-qwen3-8b-abliterated-v1",
    "context_length": 8192,
    "max_tokens": 2000,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 20,
    "repetition_penalty": 1.05,
    "system_prompt": "",
    "thinking_mode": false
}
```

**Task-Specific Overrides:**
- **Code generation:** temp=0.4, top_p=0.85, max_tokens=1500
- **Security research:** temp=0.7, top_p=0.9, max_tokens=3000
- **Reasoning:** temp=0.6, top_p=0.95, max_tokens=4096

**Warmup Command:**
```bash
opencode "Write hello world in Python"
```

**Speculative Decoding (Optional):**
- Draft model: Qwen2.5-0.5B or Qwen2.5-1.5B
- Draft tokens: 10 (0.5B) or 4 (1.5B)
- Best for: Code generation, batch processing

---

## Sources & Further Reading

### Official Documentation
- [Qwen3 Official Blog](https://qwenlm.github.io/blog/qwen3/)
- [Qwen Documentation (ReadTheDocs)](https://qwen.readthedocs.io/en/latest/)
- [Qwen3 GitHub Repository](https://github.com/QwenLM/Qwen3)
- [Qwen3-8B Hugging Face](https://huggingface.co/Qwen/Qwen3-8B)

### Context7 Resources
- [Qwen3 Library (/qwenlm/qwen3)](https://context7.com/qwenlm/qwen3/llms.txt)
- [Qwen ReadTheDocs (/websites/qwen_readthedocs_io_en)](https://qwen.readthedocs.io/)

### Speculative Decoding
- [Qwen2.5 Speculative Decoding Discussion](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct/discussions/18)
- [LM Studio Speculative Decoding Docs](https://lmstudio.ai/docs/python/llm-prediction/speculative-decoding)
- [Parasail Speculative Decoding Guide](https://docs.parasail.io/parasail-docs/dedicated/speeding-up-dedicated-models-with-speculative-decoding)

### Community Resources
- [Qwen3 Chat Template Deep Dive](https://huggingface.co/blog/qwen-3-chat-template-deep-dive)
- [Unsloth Qwen3 Guide](https://unsloth.ai/docs/models/qwen3-how-to-run-and-fine-tune)
- [Skywork AI Abliterated Models](https://skywork.ai/blog/models/)

---

**Document Version:** 1.0
**Last Updated:** 2026-02-11
**Research Scope:** Official Qwen3/Qwen2.5 documentation, Context7 technical resources, community best practices
**Model Focus:** Josiefied-Qwen3-8B-abliterated-v1 (4-bit MLX quantization)
