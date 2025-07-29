#!/usr/bin/env python3.13
"""
multi_release_formatter_llm.py

Formats summaries/{repo}.md into release_notes/{repo}_final.md using Gemini.
"""
import os
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))

SUMMARY_DIR = Path("summaries")
FINAL_DIR = Path("release_notes"); FINAL_DIR.mkdir(exist_ok=True)

for summary_file in sorted(SUMMARY_DIR.glob("*.md")):
    repo = summary_file.stem
    print(f"\n🧠 Formatting full release note for: {repo}")
    raw = summary_file.read_text()

    PROMPT = f"""
You are a product manager writing a polished, structured, and user-friendly release note.

Below is a raw changelog of features, fixes, and improvements:
{raw}

Convert it into a final release note that:
- Is well-structured with clearly labeled sections using **bold** Markdown (Slack-style)
- Uses plain English that’s easy for non-technical readers to understand
- Groups items by meaningful themes (e.g., UI, workflows, performance, integrations, QA automation, data pipelines, etc.)
- Limits to ~40 bullets TOTAL unless something is critically important
- Summarizes meaningfully rather than listing everything exhaustively
- Uses **actual emoji characters** (like 🚀 ✨ 🐛 ✅) instead of code (like `:rocket:`)
- Maintains a simple, conversational, human tone — use “you can now...” or “this helps you...” when relevant
- Specifies feature status clearly — say if something is *live*, *in progress*, or *ready but disabled*
- Uses consistent and precise naming for platforms or features (e.g., “Manthan Auto-Allocation,” “CMT,” “Superset”)
- Highlights QA/test automation improvements if present (e.g., test frameworks, isolation, reports, config design)

🧩 Use this structure:

🚀 **Overview**  
Briefly summarize what’s changed and why this release matters (2–3 short sentences max).

🔥 **What’s New**  
✨ **Features** – Major capabilities added  
🐛 **Fixes** – Key bugs resolved  
🧹 **Improvements** – Polish, performance, and usability boosts  

👉 Group bullets thematically.

💡 **Why This Matters**  
Explain how this helps users or improves decision-making, performance, or reliability.

🙌 **Special Thanks**  
Include contributor names if available. Group by roles. Give boilerplate.

Only return final Markdown-formatted output — Slack-ready and delightful.
"""
    try:
        response = model.generate_content(PROMPT)
        output_path = FINAL_DIR / f"{repo}_final.md"
        output_path.write_text(response.text.strip())
        print(f"✅ Final note saved ➜ {output_path.resolve()}")
    except Exception as e:
        print(f"❌ Error formatting {repo}: {e}")
