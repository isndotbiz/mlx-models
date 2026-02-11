#!/usr/bin/env python3
"""
Data Pipeline: Process prompt injection techniques to JSONL format
Handles outlier files with extreme token counts
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
import tiktoken
from datetime import datetime

# Configuration
SOURCE_DIR = Path("/Users/jonathanmallinger/Workspace/llm-security-research/prompts/techniques/")
OUTPUT_FILE = Path("/Users/jonathanmallinger/models/corpus_output.jsonl")
CHUNK_SIZE = 512  # tokens per chunk
OVERLAP = 50      # token overlap between chunks

# Outlier Policy: EXCLUSION LIST
# These files contain adversarial payloads with extreme token counts (22MB and 1.8MB)
# that would generate thousands of low-quality chunks
EXCLUDED_FILES = [
    "150_token80m8.md",      # ~22MB - massive encoded character payload
    "158_tokenade.md"        # ~1.8MB - large encoded character payload
]

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens using tiktoken"""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks based on token count
    Returns list of chunks with metadata
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []

    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "token_count": len(chunk_tokens),
            "start_token": start,
            "end_token": end
        })

        chunk_id += 1
        start = end - overlap if end < len(tokens) else end

    return chunks

def extract_metadata(content: str, filename: str) -> Dict[str, Any]:
    """Extract metadata from markdown frontmatter"""
    lines = content.split('\n')
    metadata = {
        "filename": filename,
        "technique_id": None,
        "slug": None,
        "source_repo": None
    }

    # Simple parser for markdown metadata
    for line in lines[:20]:  # Check first 20 lines
        if line.startswith('- **Technique ID**:'):
            metadata["technique_id"] = line.split(':')[1].strip()
        elif line.startswith('- **Slug**:'):
            metadata["slug"] = line.split(':')[1].strip()
        elif line.startswith('- **Source Repo**:'):
            metadata["source_repo"] = line.split(':')[1].strip()

    return metadata

def process_file(filepath: Path) -> List[Dict[str, Any]]:
    """Process a single markdown file into chunks"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get metadata
        metadata = extract_metadata(content, filepath.name)

        # Count total tokens
        total_tokens = count_tokens(content)

        # Create chunks
        chunks = chunk_text(content)

        # Add metadata to each chunk
        results = []
        for chunk in chunks:
            results.append({
                "source_file": filepath.name,
                "technique_id": metadata["technique_id"],
                "slug": metadata["slug"],
                "source_repo": metadata["source_repo"],
                "chunk_id": chunk["chunk_id"],
                "total_chunks": len(chunks),
                "text": chunk["text"],
                "token_count": chunk["token_count"],
                "total_file_tokens": total_tokens,
                "timestamp": datetime.utcnow().isoformat()
            })

        return results

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def validate_chunk(chunk: Dict[str, Any]) -> bool:
    """Validate that chunk has all required schema fields"""
    required_fields = [
        "source_file", "technique_id", "slug", "source_repo",
        "chunk_id", "total_chunks", "text", "token_count",
        "total_file_tokens", "timestamp"
    ]
    return all(field in chunk for field in required_fields)

def main():
    """Main processing pipeline"""
    print("=" * 80)
    print("DATA PIPELINE: CORPUS PROCESSING")
    print("=" * 80)

    # Count source files
    all_files = list(SOURCE_DIR.glob("*.md"))
    print(f"\nSOURCE DIRECTORY: {SOURCE_DIR}")
    print(f"Total markdown files: {len(all_files)}")

    # Calculate total size
    total_size = sum(f.stat().st_size for f in all_files)
    print(f"Total size: {total_size / (1024*1024):.2f} MB")

    # Identify outliers
    print(f"\nOUTLIER POLICY: EXCLUSION")
    print(f"Files excluded from processing: {len(EXCLUDED_FILES)}")
    for excluded in EXCLUDED_FILES:
        excluded_path = SOURCE_DIR / excluded
        if excluded_path.exists():
            size_mb = excluded_path.stat().st_size / (1024*1024)
            print(f"  - {excluded}: {size_mb:.2f} MB")

    # Filter files
    files_to_process = [f for f in all_files if f.name not in EXCLUDED_FILES]
    print(f"\nFiles to process: {len(files_to_process)}")

    # Process files
    all_chunks = []
    print("\nProcessing files...")
    for filepath in files_to_process:
        chunks = process_file(filepath)
        all_chunks.extend(chunks)
        print(f"  {filepath.name}: {len(chunks)} chunks")

    # Write JSONL output
    print(f"\nWriting output to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + '\n')

    output_size_mb = OUTPUT_FILE.stat().st_size / (1024*1024)
    print(f"Output file size: {output_size_mb:.2f} MB")

    # Validation
    print("\n" + "=" * 80)
    print("VALIDATION")
    print("=" * 80)

    # Schema validation
    schema_valid = all(validate_chunk(chunk) for chunk in all_chunks)
    print(f"Schema validation: {'PASS' if schema_valid else 'FAIL'}")

    # Statistics
    print(f"\nTotal chunks generated: {len(all_chunks)}")
    token_counts = [chunk["token_count"] for chunk in all_chunks]
    print(f"Chunk token count distribution:")
    print(f"  Min: {min(token_counts)}")
    print(f"  Max: {max(token_counts)}")
    print(f"  Mean: {sum(token_counts) / len(token_counts):.2f}")

    # Sample quality check
    print(f"\nSample quality check (10 random chunks):")
    import random
    random.seed(42)
    samples = random.sample(all_chunks, min(10, len(all_chunks)))

    quality_pass = True
    for i, sample in enumerate(samples, 1):
        has_text = len(sample["text"].strip()) > 0
        has_tokens = sample["token_count"] > 0
        has_metadata = sample["technique_id"] is not None

        status = "OK" if (has_text and has_tokens) else "FAIL"
        if status == "FAIL":
            quality_pass = False

        print(f"  Sample {i}: {sample['source_file'][:30]:30s} | "
              f"Tokens: {sample['token_count']:4d} | "
              f"Text len: {len(sample['text']):5d} | "
              f"Status: {status}")

    print(f"\nQuality check: {'PASS' if quality_pass else 'FAIL'}")

    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
