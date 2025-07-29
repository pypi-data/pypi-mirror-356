#!/usr/bin/env python3
"""
multi_post_release_notes_to_slack.py

Posts each release_notes/{repo}_final.md to Slack with the repo name as a header.
"""

import os, re, requests
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTES_DIR = Path("release_notes")

if not SLACK_WEBHOOK_URL:
    raise SystemExit("❌ SLACK_WEBHOOK_URL missing in .env")

md_files = sorted(NOTES_DIR.glob("*_final.md"))
if not md_files:
    raise SystemExit("❌ No final release notes found in release_notes/")

for path in md_files:
    repo = path.stem.replace("_final", "")
    text = path.read_text()

    # Clean up for Slack format
    text = re.sub(r"\*\*(.+?):\*\*", r"**\1**:", text)  # fix headings
    text = text.replace("**", "*").replace("*   ", "• ").replace("* ", "• ")

    full_message = f"*📦 Release Notes: `{repo}`*\n{text}"

    print(f"\n📤 Posting developer release note for {repo} …")
    r = requests.post(SLACK_WEBHOOK_URL, json={"text": full_message})
    if r.status_code == 200:
        print(f"✅ Posted {repo} release note to Slack!")
    else:
        print(f"❌ Failed for {repo}. Status: {r.status_code}, Response: {r.text}")
