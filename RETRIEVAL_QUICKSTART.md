# Retrieval System Quick Start Guide

## 🚀 Running the Tests

### Basic Usage
```bash
cd /Users/jonathanmallinger/models
python3 retrieval_smoke_test.py
```

### Expected Output
```
🚀 Starting Retrieval & Smoke Tests - Agent E
============================================================

📋 Running smoke tests on 5 diverse queries...

🔍 Testing: 'jailbreak technique for Claude'
  Top-1: claude_jailbreaks.md | RRF: 0.0164 | Relevance: HIGH
  ...

✅ PASS
```

---

## 📊 Understanding Results

### RRF Scores
- **Range**: 0.0154 - 0.0164 (typical)
- **Higher = Better**: Top results score ~0.0164
- **Formula**: `1 / (k + rank)` where k=60

### Relevance Levels
- **HIGH**: Query terms match 70%+ of content
- **MED**: Query terms match 40-70% of content
- **LOW**: Query terms match <40% of content

### Latency Benchmarks
- **First Query**: ~0.03s (initialization)
- **Subsequent**: ~0.0001s (cached)
- **Target**: < 5s per query

---

## 🔧 Configuration

### Adjusting Alpha (Fusion Weight)

```python
# Pure Dense (FAISS semantic search)
retriever = HybridRetriever(alpha=1.0)

# Pure Sparse (BM25 keyword search)
retriever = HybridRetriever(alpha=0.0)

# Balanced Hybrid (recommended)
retriever = HybridRetriever(alpha=0.6)
```

### Changing Top-K

```python
# Get more results
results, latency = retriever.retrieve(query, top_k=10)

# Get fewer results
results, latency = retriever.retrieve(query, top_k=3)
```

### Adjusting RRF Parameter

```python
# Modify in HybridRetriever.__init__()
self.k = 60  # Default (lower = more aggressive ranking)
self.k = 100 # More conservative ranking
```

---

## 🧪 Custom Test Queries

### Add Your Own Queries

Edit the `test_queries` list in `main()`:

```python
test_queries = [
    "your custom query here",
    "another test query",
    # ... add more
]
```

### Run Single Query

```python
from retrieval_smoke_test import HybridRetriever

retriever = HybridRetriever(alpha=0.6)
results, latency = retriever.retrieve("test query", top_k=5)

for result in results:
    print(f"{result.rank}. {result.filename} (RRF: {result.rrf_score:.4f})")
```

---

## 📁 Output Files

### JSON Results
**Location**: `/Users/jonathanmallinger/models/retrieval_test_results.json`

**Structure**:
```json
{
  "queries": [...],
  "fusion_tests": {...},
  "metadata_integrity": {...}
}
```

### Validation Report
**Location**: `/Users/jonathanmallinger/models/RETRIEVAL_VALIDATION_REPORT.md`

Contains detailed analysis of all tests.

---

## 🔍 Understanding the Database

### Current Documents (9 total)

1. **claude_jailbreaks.md** - System prompt extraction for Claude
2. **gpt_vulnerabilities.md** - GPT-5 specific attacks
3. **eni_persona_attack.md** - Persona manipulation techniques
4. **deepseek_reasoning.md** - Reasoning model exploits
5. **chain_of_draft.md** - Iterative refinement attacks
6. **claude_developer_mode.md** - DAN-style roleplay
7. **anthropic_constitutional.md** - Constitutional AI bypass
8. **prompt_injection_guide.md** - Universal injection techniques
9. **openai_alignment_weaknesses.md** - RLHF exploitation

### Document Structure
```python
{
    "filename": "example.md",
    "technique_name": "Attack Name",
    "section": "Category",
    "content": "Full text description..."
}
```

---

## 🛠 Extending the System

### Add New Documents

Edit `MockJailbreakDatabase.__init__()`:

```python
self.documents.append({
    "filename": "new_attack.md",
    "technique_name": "Novel Attack Vector",
    "section": "Advanced Techniques",
    "content": "Description of the attack..."
})
```

### Implement Real FAISS Index

```python
import faiss
import numpy as np

class ProductionRetriever(HybridRetriever):
    def __init__(self, index_path: str, alpha: float = 0.6):
        super().__init__(alpha)
        self.index = faiss.read_index(index_path)
        self.embeddings = self._load_embeddings()

    def _simulate_dense_retrieval(self, query: str, top_k: int):
        # Replace with actual FAISS search
        query_embedding = self._embed(query)
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            top_k
        )
        # Process results...
```

### Implement Real BM25 Index

```python
from rank_bm25 import BM25Okapi

class ProductionRetriever(HybridRetriever):
    def __init__(self, corpus: List[str], alpha: float = 0.6):
        super().__init__(alpha)
        tokenized_corpus = [doc.split() for doc in corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def _simulate_sparse_retrieval(self, query: str, top_k: int):
        # Replace with actual BM25 search
        scores = self.bm25.get_scores(query.split())
        top_indices = np.argsort(scores)[-top_k:][::-1]
        # Process results...
```

---

## 📈 Performance Tuning

### Optimize Alpha Value

Test different values to find optimal fusion:

```python
alphas = [0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 1.0]

for alpha in alphas:
    retriever = HybridRetriever(alpha=alpha)
    results, _ = retriever.retrieve("test query")
    print(f"Alpha {alpha}: {results[0].filename}")
```

### Benchmark Latency

```python
import time

queries = ["query1", "query2", ...]
retriever = HybridRetriever(alpha=0.6)

latencies = []
for query in queries:
    start = time.time()
    results, _ = retriever.retrieve(query)
    latencies.append(time.time() - start)

print(f"Avg latency: {np.mean(latencies):.4f}s")
print(f"P95 latency: {np.percentile(latencies, 95):.4f}s")
```

---

## ✅ Validation Checklist

When modifying the system, ensure:

- [ ] All queries return results
- [ ] RRF scores are differentiated (not all identical)
- [ ] Metadata fields populated (filename, technique_name, section)
- [ ] Fusion behavior differs (α=0.0 ≠ α=0.6 ≠ α=1.0)
- [ ] Latency < 5s per query
- [ ] Top-1 results have HIGH or MED relevance

Run validation:
```bash
python3 retrieval_smoke_test.py
```

Check for: `✅ PASS` in output.

---

## 🐛 Troubleshooting

### Issue: All RRF scores identical
**Cause**: Dense and sparse retrievers returning same ranking
**Fix**: Adjust scoring logic to differentiate semantic vs keyword matching

### Issue: Latency > 5s
**Cause**: Large document corpus or slow vector operations
**Fix**: Implement FAISS approximate search, add caching

### Issue: Low relevance scores
**Cause**: Poor query-document matching
**Fix**: Tune alpha parameter, improve document coverage

### Issue: Missing metadata
**Cause**: Document structure incomplete
**Fix**: Verify all documents have required fields

---

## 📚 Further Reading

### Related Files
- `retrieval_smoke_test.py` - Main test implementation
- `RETRIEVAL_VALIDATION_REPORT.md` - Detailed analysis
- `retrieval_test_results.json` - Raw test data

### Key Concepts
- **RRF (Reciprocal Rank Fusion)**: Score fusion algorithm
- **FAISS**: Dense vector similarity search
- **BM25**: Sparse keyword-based retrieval
- **Hybrid Retrieval**: Combining dense + sparse signals

### References
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)
- [RRF Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

---

**Last Updated**: 2026-02-11
**Maintainer**: Agent E (Retrieval & Smoke Tests)
