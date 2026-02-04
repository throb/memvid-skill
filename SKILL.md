# Memvid Memory Skill

Search Bob's memory using Memvid. Fast text search across MEMORY.md, daily logs, workspace docs, and conversation history.

## When to Use
- Questions about past conversations, decisions, or context
- "What did we discuss about X?"
- "When did Rob mention Y?"
- Looking up prior work, projects, or preferences

## Quick Search

```bash
cd ~/clawd/skills/memvid-memory && source ~/.bashrc && python3.10 scripts/search.py "your query here"
```

## Commands

### Search (semantic + lexical hybrid)
```bash
python3.10 scripts/search.py "query" [--k 5] [--mode hybrid|semantic|lex]
```

### Rebuild Index
```bash
python3.10 scripts/rebuild.py
```

Rebuilds the memory index from:
- MEMORY.md (long-term memory)
- TOOLS.md, USER.md, IDENTITY.md
- memory/*.md (daily logs)

## Memory File Location
`~/clawd/memvid-memory/bob.mv2`

## Technical Details
- Embeddings: OpenAI text-embedding-3-small (1536 dim)
- Requires OPENAI_API_KEY in environment
- Hybrid search combines semantic similarity + BM25 text matching
