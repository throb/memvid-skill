#!/usr/bin/env python3
"""Search memvid memory index."""

import sys
import memvid_sdk
from pathlib import Path

INDEX = Path(__file__).parent.parent / "bob.mv2"

def search(query: str, mode: str = "semantic", k: int = 5):
    """Search the memory index."""
    if not INDEX.exists():
        print(f"Error: Index not found at {INDEX}")
        print("Run rebuild.py first")
        sys.exit(1)
    
    # Enable vec for semantic search
    m = memvid_sdk.use("basic", str(INDEX), enable_vec=(mode == "semantic"))
    results = m.find(query, mode=mode, k=k)
    
    print(f"Query: {query}")
    print(f"Mode: {mode}")
    print(f"Results: {len(results['hits'])}")
    print("-" * 60)
    
    for hit in results['hits']:
        score = hit['score']
        title = hit['title']
        snippet = hit['snippet'][:200].replace('\n', ' ')
        print(f"[{score:.3f}] {title}")
        print(f"  {snippet}...")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [mode] [k]")
        print("  mode: semantic (default) or lex")
        print("  k: number of results (default 5)")
        sys.exit(1)
    
    query = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "semantic"
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    search(query, mode, k)
