#!/usr/bin/env python3
"""
multi_commit_cleaner.py

Cleans all raw commit files under `commits/` and outputs cleaned versions
to `cleaned_commits/` with the same base filename.
"""

import os
import re
import json
from pathlib import Path

RAW_DIR = Path("commits")
CLEAN_DIR = Path("cleaned_commits")
CLEAN_DIR.mkdir(exist_ok=True)

def clean_comment(comment: str) -> str:
    comment = re.sub(r"ID:[^;]+;HOURS:\d+;DONE:\d+;?\s*", "", comment, flags=re.IGNORECASE)
    comment = re.sub(r"^Merged PR \d+: ?", "", comment, flags=re.IGNORECASE)

    if "merge remote-tracking branch" in comment.lower() or "merge branch" in comment.lower():
        return ""

    if any(w in comment.lower() for w in ["sit deploy", "sit deployment", "testing", "deployment", "test cases", "testcase"]):
        return ""

    if re.fullmatch(r"(fix|fixes|changes|reverted|hotfixes|hotfix|prod changes|removes|remove|cleanup|skiped|skip)", comment.strip().lower()):
        return ""

    return comment.strip()

def process_file(file_path: Path):
    with file_path.open() as f:
        commits = json.load(f)

    cleaned_comments = set()
    cleaned_commits = []

    for entry in commits:
        raw_comment = entry.get("comment", "")
        cleaned = clean_comment(raw_comment)

        if cleaned and cleaned.lower() not in cleaned_comments:
            cleaned_comments.add(cleaned.lower())
            cleaned_commits.append({
                "commitId": entry.get("commitId"),
                "author": entry.get("author"),
                "date": entry.get("date"),
                "comment": cleaned
            })

    output_file = CLEAN_DIR / file_path.name.replace("release_commits", "cleaned_commits")
    with output_file.open("w") as f:
        json.dump(cleaned_commits, f, indent=2)

    print(f"✅ Cleaned {len(cleaned_commits)} → {output_file.name}")

def main():
    files = list(RAW_DIR.glob("*_release_commits.json"))
    if not files:
        print("❌ No raw commit files found in 'commits/' directory.")
        return

    for file in files:
        process_file(file)

if __name__ == "__main__":
    main()
