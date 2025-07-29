#!/usr/bin/env python3.13
"""
multi_commit_summarizer.py

Summarizes each repo’s commit chunks into a markdown mini-release note.
Each summary is saved under summaries/{repo}.md
"""

import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()

# ── Setup ─────────────────────────────────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))

CHUNK_DIR = Path("chunks")
SUMMARY_DIR = Path("summaries")
SUMMARY_DIR.mkdir(exist_ok=True)

PROMPT = (
    "You are a release-note assistant. Read the raw commit list and produce a"
    " brief, user-friendly changelog with three sections:"
    "  ✨ Features, 🐛 Fixes, 🧹 Improvements."
    " • Use simple language\n• Drop internal IDs / times / PR numbers\n"
    " • Bullet points only.\n\nRAW COMMITS:\n{chunk}"
)

# ── Process ────────────────────────────────────────────────────────────────
repo_dirs = [d for d in CHUNK_DIR.iterdir() if d.is_dir()]
if not repo_dirs:
    raise SystemExit("❌ No repo chunk folders found in /chunks")

for repo_dir in repo_dirs:
    repo_name = repo_dir.name
    print(f"\n📁 Summarizing {repo_name} …")

    summary_path = SUMMARY_DIR / f"{repo_name}.md"
    summary_path.write_text("")  # Clear previous run

    chunk_files = sorted(repo_dir.glob("chunk_*.txt"))
    for idx, chunk_file in enumerate(chunk_files, 1):
        print(f"🤖  Summarizing {chunk_file.name} …")
        try:
            chunk = chunk_file.read_text()
            response = model.generate_content(PROMPT.format(chunk=chunk))
            with open(summary_path, "a", encoding="utf-8") as f:
                f.write(f"## Chunk {idx}\n{response.text.strip()}\n\n")
        except Exception as e:
            print(f"❌  Error summarizing {chunk_file.name}: {e}")

    print(f"✅  Summary saved: {summary_path.resolve()}")
