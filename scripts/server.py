#!/usr/bin/env python3
"""MCP Server for MemVid Memory.

Exposes memory search and reading capabilities to MCP clients (like Claude Code).
"""

import sys
import os
import memvid_sdk
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load env vars from .env file
load_dotenv(Path(__file__).parent.parent / ".env")

# Define paths
WORKSPACE = Path.home() / "clawd"
INDEX_PATH = WORKSPACE / "skills" / "memvid-memory" / "bob.mv2"

# Initialize MCP server
mcp = FastMCP("memvid-memory")

@mcp.tool()
def search_memory(query: str, k: int = 5) -> str:
    """Search your long-term memory (MemVid index).
    
    Use this to recall past conversations, project details, user preferences,
    or specific facts stored in the memory system.
    
    Args:
        query: The search query string.
        k: Number of results to return (default 5).
    """
    if not INDEX_PATH.exists():
        return f"Error: Memory index not found at {INDEX_PATH}. Please run rebuild first."
    
    # Initialize MemVid
    # Note: enable_vec=True requires OPENAI_API_KEY in env
    try:
        m = memvid_sdk.use("basic", str(INDEX_PATH), enable_vec=True)
        results = m.find(query, mode="semantic", k=k)
    except Exception as e:
        return f"Error searching memory: {str(e)}"
    
    output = []
    output.append(f"Found {len(results['hits'])} results for '{query}':\n")
    
    for hit in results['hits']:
        score = hit['score']
        title = hit['title']
        snippet = hit['snippet'].replace('\n', ' ')
        
        # Add date context if available in title
        date_hint = ""
        if title.startswith("20") and title.endswith(".md"):
            date_hint = f" [DATE: {title.replace('.md', '')}]"
        elif title == "MEMORY.md":
            date_hint = " [SOURCE: CORE MEMORY]"
            
        output.append(f"[{score:.3f}] {title}{date_hint}")
        output.append(f"  {snippet}...")
        output.append("")
        
    return "\n".join(output)

@mcp.tool()
def read_memory_file(filename: str) -> str:
    """Read the full content of a specific memory file.
    
    Use this when search results point to a file (like '2026-02-04.md') 
    and you need the full context of that day/document.
    
    Args:
        filename: The name of the file (e.g., '2026-02-04.md' or 'MEMORY.md').
    """
    # Check common locations
    locations = [
        WORKSPACE / filename,
        WORKSPACE / "memory" / filename,
        WORKSPACE / "archive" / filename
    ]
    
    for loc in locations:
        if loc.exists() and loc.is_file():
            return loc.read_text()
            
    return f"Error: File '{filename}' not found in workspace memory paths."

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is present
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required (check .env file)", file=sys.stderr)
        sys.exit(1)
        
    mcp.run()
