#!/usr/bin/env python3
"""
multi_commit_chunker.py

Chunks cleaned commit messages from multiple repositories into smaller text files
for LLM summarization. Output is saved in chunks/{repo_name}/chunk_{i}.txt
"""

import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ── Constants ─────────────────────────────────────────────────────────────
CLEANED_DIR = Path("cleaned_commits")
CHUNKS_DIR = Path("chunks")
TOK_MAX = 1_000_000
CHUNK_TOK = int(TOK_MAX * 0.40)
WORDS_CH = int(CHUNK_TOK * 3.3)  # ≈ 13,200 words per chunk

# ── Execution ─────────────────────────────────────────────────────────────
if not CLEANED_DIR.exists():
    print(f"❌ Directory not found: {CLEANED_DIR.resolve()}")
    exit(1)

files = list(CLEANED_DIR.glob("*.json"))
if not files:
    print("⚠️  No cleaned commit files found.")
    exit(0)

for infile in files:
    repo_name = infile.stem.replace("_cleaned_commits", "")
    print(f"\n📂 Processing repo: {repo_name}")

    with open(infile) as f:
        comments = [c["comment"].strip() for c in json.load(f) if c.get("comment")]

    if not comments:
        print(f"⚠️  No comments to chunk in {repo_name}")
        continue

    chunks, buf, words = [], [], 0
    for msg in comments:
        w = len(msg.split())
        if words + w > WORDS_CH:
            chunks.append("\n".join(buf)); buf, words = [], 0
        buf.append(f"- {msg}"); words += w
    if buf: chunks.append("\n".join(buf))

    repo_chunk_dir = CHUNKS_DIR / repo_name
    repo_chunk_dir.mkdir(parents=True, exist_ok=True)

    for i, txt in enumerate(chunks, 1):
        path = repo_chunk_dir / f"chunk_{i}.txt"
        path.write_text(txt)
        print(f"📦 Created: {path}")

print(f"\n✅ Completed chunking for {len(files)} repo(s). All chunks saved in '{CHUNKS_DIR}/'")
