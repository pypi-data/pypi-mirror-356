#!/usr/bin/env python3.13
"""
Azure DevOps multi-repo commit fetcher:
• Reads repo_config.json with last_commit_sha per repo
• Fetches latest commit from Azure DevOps for each repo
• Fetches all commits between last_commit_sha and latest commit
• Saves each repo's commits to commits/{repo_name}_release_commits.json
• Does NOT update repo_config.json (done separately to ensure safety)
"""

import os, json, time, requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── env vars ─────────────────────────────────────────────────────────────
AZ_ORG  = os.getenv("AZ_ORG")     or os.getenv("AZURE_ORG_URL", "").rstrip("/").split("/")[-1]
AZ_PROJ = os.getenv("AZ_PROJECT") or os.getenv("PROJECT_NAME")
AZ_PAT  = os.getenv("AZ_PAT")     or os.getenv("AZURE_PAT")

if not AZ_ORG or not AZ_PROJ or not AZ_PAT:
    raise SystemExit("❌ Missing one or more env vars: AZ_ORG, AZ_PROJECT, AZ_PAT")

# ── setup ─────────────────────────────────────────────────────────────────
HEADERS = {"Accept": "application/json"}
SESSION = requests.Session(); SESSION.auth = ("", AZ_PAT)
PAGE, RETRY, BACK = 100, 3, 2

repo_config = json.loads(Path("repo_config.json").read_text())
Path("commits").mkdir(exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────
def az_get(url, **params):
    for attempt in range(1, RETRY + 1):
        try:
            r = SESSION.get(url, headers=HEADERS, params=params, timeout=15)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError):
            time.sleep(BACK ** attempt)
        except requests.HTTPError as e:
            if r.status_code in (429, 502, 503, 504):
                time.sleep(BACK ** attempt)
            else:
                raise RuntimeError(f"Azure {r.status_code}: {r.text[:200]}") from e
    raise RuntimeError("Azure API repeatedly failed")

def get_latest_commit_sha(repo_id):
    url = f"https://dev.azure.com/{AZ_ORG}/{AZ_PROJ}/_apis/git/repositories/{repo_id}/commits"
    result = az_get(url, **{"$top": 1, "api-version": "7.0"})
    if not result.get("value"): return None
    return result["value"][0]["commitId"]

def fetch_commits(repo_id, from_sha, to_sha):
    url = f"https://dev.azure.com/{AZ_ORG}/{AZ_PROJ}/_apis/git/repositories/{repo_id}/commits"
    params = {
        "searchCriteria.itemVersion.versionType": "commit",
        "searchCriteria.itemVersion.version": from_sha,
        "searchCriteria.compareVersion.versionType": "commit",
        "searchCriteria.compareVersion.version": to_sha,
        "$top": PAGE,
        "api-version": "7.0"
    }

    all_commits, skip = [], 0
    while True:
        batch = az_get(url, **params, **{"$skip": skip}).get("value", [])
        all_commits.extend(batch)
        if len(batch) < PAGE:
            break
        skip += PAGE
    return all_commits

# ── main ─────────────────────────────────────────────────────────────────
for repo_name, conf in repo_config.items():
    repo_id = conf.get("repo_id")
    from_sha = conf.get("last_commit_sha")

    if not repo_id or not from_sha:
        print(f"⚠️  Skipping {repo_name} – Missing repo_id or last_commit_sha")
        continue

    try:
        print(f"\n🔍 {repo_name}: checking latest commit …")
        to_sha = get_latest_commit_sha(repo_id)
        if not to_sha:
            print(f"❌  Could not find latest commit for {repo_name}")
            continue

        print(f"🔄  Fetching commits {from_sha[:7]} → {to_sha[:7]}")
        commits = fetch_commits(repo_id, from_sha, to_sha)
        print(f"📄  {len(commits)} commits found.")

        cleaned = []
        for c in commits:
            cleaned.append(dict(
                commitId=c["commitId"],
                author=c.get("author", {}).get("name", "unknown"),
                date=c.get("author", {}).get("date", ""),
                comment=c.get("comment", "").strip()
            ))

        out_file = f"commits/{repo_name}_release_commits.json"
        with open(out_file, "w") as f:
            json.dump(cleaned, f, indent=2)

        print(f"✅  Saved to {out_file}")

    except Exception as e:
        print(f"❌  Error in {repo_name}: {e}")
