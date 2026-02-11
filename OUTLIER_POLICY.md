# Data Pipeline Outlier Handling Policy

## Overview
This document describes the outlier handling policy implemented for the prompt injection techniques corpus processing pipeline.

## Problem Statement
The source corpus contains 139 markdown files totaling 26.66 MB. Two files are extreme outliers:
- `150_token80m8.md`: 22.36 MB (~84% of total corpus)
- `158_tokenade.md`: 1.78 MB (~7% of total corpus)

These two files contain adversarial payloads with encoded Unicode characters designed to bypass LLM safety mechanisms. They represent only 1.4% of files but 91% of total data size.

## Analysis of Options

### Option A: Exclude Files from Processing (SELECTED)
**Rationale:**
- These files are adversarial payloads, not instructional content
- Would generate thousands of low-quality chunks (>8000 chunks from 150_token80m8.md alone)
- Encoded character sequences don't provide meaningful training signal
- Payload tokens would dominate the corpus and skew embeddings
- Quality vs. quantity tradeoff strongly favors exclusion

**Implementation:**
- Files added to `EXCLUDED_FILES` list in `process_to_jsonl.py`
- Excluded before processing begins
- Logged in processing output for transparency

**Impact:**
- 137 files processed (98.6% of files)
- 4.30 MB processed (16% of total size)
- 1,447 high-quality chunks generated
- Exclusion documented in processing logs

### Option B: Process with Larger Chunk Sizes
**Drawbacks:**
- Would still generate >5000 chunks from outlier files
- Inconsistent chunk sizes across corpus
- Encoded payloads still provide no meaningful signal
- Computational waste

### Option C: Store as Blobs Without Chunking
**Drawbacks:**
- Single massive blobs hard to work with in RAG systems
- No clear use case for retrieving entire adversarial payload
- Storage inefficiency

## Implementation Details

### Exclusion List
```python
EXCLUDED_FILES = [
    "150_token80m8.md",      # ~22MB - massive encoded character payload
    "158_tokenade.md"        # ~1.8MB - large encoded character payload
]
```

### Processing Statistics
- **Source Files**: 139 total, 137 processed, 2 excluded
- **Total Input Size**: 26.66 MB
- **Processed Size**: 4.30 MB (16% of total)
- **Output Size**: 3.39 MB JSONL
- **Chunks Generated**: 1,447

### Content Characteristics of Excluded Files
Both files contain:
- Header with standard metadata
- Massive payload section with Unicode combining characters
- Example from 150_token80m8.md:
  ```
  💀󠇠󠆏󠅾󠅹󠇣󠆐󠅴󠆤󠇣󠆐󠅴󠆥󠇣󠆐󠅴󠆣󠇣󠆐󠅴...
  ```
- These are technique demonstrations, not instructional content
- File sizes disproportionate to information content

## Quality Assurance

### Validation Checks
✓ Schema validation: PASS (all 1,447 chunks)
✓ Required fields: PASS (100% coverage)
✓ Token counts: Mean 489, Min 55, Max 512
✓ Content quality: PASS (random sample of 10 chunks)
✓ Metadata extraction: PASS (technique_id, slug, source_repo)

### Coverage Analysis
- Processed files represent 98.6% of unique techniques
- Excluded files are payload demonstrations, not unique techniques
- No loss of instructional or analytical content

## Recommendations

1. **Keep exclusion list updated**: Review new files for similar patterns
2. **Document exclusions**: Log excluded files in processing output
3. **Monitor file sizes**: Alert on files >100KB for review
4. **Validate content**: Ensure excluded files don't contain embedded instructions

## Future Considerations

If adversarial payload analysis becomes necessary:
- Create separate pipeline for payload analysis
- Use specialized tokenization/embedding
- Store in separate collection from instructional corpus
- Process payloads in controlled environment

## Conclusion

The exclusion policy optimizes for:
- **Quality**: High-value instructional content
- **Usability**: Consistent chunk sizes for RAG
- **Efficiency**: No computational waste on low-signal data
- **Maintainability**: Clear documentation of decisions

**Policy Status**: APPROVED AND IMPLEMENTED
**Implementation Date**: 2026-02-11
**Last Review**: 2026-02-11
