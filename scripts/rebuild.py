#!/usr/bin/env python3
"""Rebuild memvid memory index from workspace files + beads issues."""

import json
import memvid_sdk
from pathlib import Path

WORKSPACE = Path.home() / "clawd"
OUTPUT = Path(__file__).parent.parent / "bob.mv2"

# Remove old file if exists
if OUTPUT.exists():
    OUTPUT.unlink()

# Files to index
files = [
    WORKSPACE / "MEMORY.md",
    WORKSPACE / "TOOLS.md", 
    WORKSPACE / "USER.md",
    WORKSPACE / "IDENTITY.md",
    WORKSPACE / "AGENTS.md",
    WORKSPACE / "SOUL.md",
]

# Add daily memory logs
memory_dir = WORKSPACE / "memory"
if memory_dir.exists():
    files.extend(sorted(memory_dir.glob("*.md")))

# Add archived memory logs
archive_dir = WORKSPACE / "archive"
if archive_dir.exists():
    files.extend(sorted(archive_dir.glob("*.md")))

# Create with vector index enabled (uses OpenAI embeddings by default)
print(f"Creating {OUTPUT} with OpenAI embeddings...")
m = memvid_sdk.create(str(OUTPUT), enable_vec=True, enable_lex=True)

# Index markdown files
for f in files:
    if f.exists():
        text = f.read_text()
        m.put(title=f.name, text=text, enable_embedding=True, embedding_model="openai-small")
        print(f"Added: {f.name} ({len(text):,} bytes)")

# Index Beads issues
beads_jsonl = WORKSPACE / ".beads" / "issues.jsonl"
if beads_jsonl.exists():
    print(f"\nIndexing Beads issues from {beads_jsonl}...")
    issue_count = 0
    with open(beads_jsonl) as f:
        for line in f:
            try:
                issue = json.loads(line)
                # Build searchable text from issue
                title = issue.get("title", "")
                desc = issue.get("description", "")
                labels = ", ".join(issue.get("labels", []))
                status = issue.get("status", "")
                priority = issue.get("priority", "")
                issue_id = issue.get("id", "")
                
                text = f"""Issue: {issue_id}
Title: {title}
Status: {status}
Priority: {priority}
Labels: {labels}
Description: {desc}"""
                
                m.put(
                    title=f"Issue: {issue_id} - {title}",
                    text=text,
                    tags=issue.get("labels", []),
                    enable_embedding=True,
                    embedding_model="openai-small"
                )
                issue_count += 1
            except json.JSONDecodeError:
                continue
    print(f"Added: {issue_count} Beads issues")

# Get stats before sealing
stats = m.stats()
print(f"\nStats: {stats}")

# Seal and close to save
m.seal()
m.close()
print(f"Done! Created {OUTPUT}")
