#!/usr/bin/env python3
"""
multi_post_user_notes_to_slack.py

Posts each user_release_notes/{repo}_user.md to Slack with repo name as header.
"""

import os, re, requests
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTES_DIR = Path("user_release_notes")

if not SLACK_WEBHOOK_URL:
    raise SystemExit("❌ SLACK_WEBHOOK_URL missing in .env")

md_files = sorted(NOTES_DIR.glob("*_user.md"))
if not md_files:
    raise SystemExit("❌ No user release notes found in user_release_notes/")

for path in md_files:
    repo = path.stem.replace("_user", "")
    text = path.read_text()

    # Format for Slack
    text = re.sub(r"\*\*(.+?):\*\*", r"**\1**:", text)
    text = text.replace("**", "*").replace("*   ", "• ").replace("* ", "• ")

    full_message = f"*🧑‍💻 User Release Notes: `{repo}`*\n{text}"

    print(f"\n📤 Posting user release note for {repo} …")
    r = requests.post(SLACK_WEBHOOK_URL, json={"text": full_message})
    if r.status_code == 200:
        print(f"✅ Posted user note for {repo} to Slack!")
    else:
        print(f"❌ Failed for {repo}. Status: {r.status_code}, Response: {r.text}")
