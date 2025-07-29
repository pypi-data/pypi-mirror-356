# release_note_automator/cli.py

#!/usr/bin/env python3

import os, json, requests, subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import set_key, load_dotenv

try:
    import questionary
except ImportError:
    print("Installing questionary…")
    os.system("pip install questionary wcwidth")
    import questionary

def main():
    load_dotenv()

    AZ_ORG = os.getenv("AZ_ORG") or questionary.text("🔐 Enter your Azure DevOps Org:").ask()
    AZ_PROJECT = os.getenv("AZ_PROJECT") or questionary.text("📂 Enter your Azure Project:").ask()
    AZ_PAT = os.getenv("AZ_PAT") or questionary.password("🔑 Enter your Azure PAT:").ask()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or questionary.password("🔮 Enter your Google Gemini API Key:").ask()

    cutoff_days = int(questionary.text("📅 How many days of history should be considered? (e.g., 7 or 14)").ask())
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=cutoff_days)

    # Save to .env
    env_file = Path(".env")
    env_file.write_text("")
    set_key(str(env_file), "AZ_ORG", AZ_ORG)
    set_key(str(env_file), "AZ_PROJECT", AZ_PROJECT)
    set_key(str(env_file), "AZ_PAT", AZ_PAT)
    set_key(str(env_file), "GEMINI_API_KEY", GEMINI_API_KEY)
    print(f"\n📝 Saved credentials to {env_file.resolve()}")

    # Fetch repos
    print("\n📡 Fetching repositories from Azure DevOps...")
    headers = {"Accept": "application/json"}
    session = requests.Session(); session.auth = ("", AZ_PAT)
    url = f"https://dev.azure.com/{AZ_ORG}/{AZ_PROJECT}/_apis/git/repositories?api-version=7.0"
    res = session.get(url, headers=headers)
    res.raise_for_status()
    all_repos = res.json()["value"]

    repo_choices = [f"{r['name']} ({r['id']})" for r in all_repos]
    selected = questionary.checkbox("✅ Select repositories to track:", choices=repo_choices).ask()
    selected_ids = {i.split(" (")[0]: i.split(" (")[1][:-1] for i in selected}

    config = {}
    now = datetime.now(timezone.utc)
    print("\n📦 Fetching starting commits …")

    for name, repo_id in selected_ids.items():
        found_commit = None
        from_commit_date = None

        for branch in ["master", "main"]:
            try:
                commits_url = f"https://dev.azure.com/{AZ_ORG}/{AZ_PROJECT}/_apis/git/repositories/{repo_id}/commits"
                params = {
                    "searchCriteria.toDate": cutoff_date.isoformat(),
                    "searchCriteria.$top": 1,
                    "searchCriteria.itemVersion.versionType": "branch",
                    "searchCriteria.itemVersion.version": branch,
                    "api-version": "7.0"
                }
                r = session.get(commits_url, headers=headers, params=params)
                r.raise_for_status()
                commits = r.json().get("value", [])

                if commits:
                    found_commit = commits[0]
                    from_commit_date = found_commit["author"]["date"]
                    break
            except:
                continue

        if not found_commit:
            print(f"❌ Error for {name}: No commits found before {cutoff_days} days ago or no valid branch.")
            continue

        config[name] = {
            "repo_id": repo_id,
            "last_commit_sha": found_commit["commitId"],
            "last_processed_time": now.isoformat(),
            "from_commit_date": from_commit_date,
            "to_commit_date": now.isoformat()
        }

        from_dt = datetime.fromisoformat(from_commit_date).strftime("%d %b %Y (%A)")
        print(f"✅ {name} → SHA: {found_commit['commitId'][:7]} (starting from: {from_dt})")

    Path("repo_config.json").write_text(json.dumps(config, indent=2))
    print(f"\n🗂️  repo_config.json written with {len(config)} repos.")

    # Run pipeline
    print("\n🚀 Running release note pipeline …\n")
    scripts = [
        "multi_commit_fetcher.py",
        "multi_commit_cleaner.py",
        "multi_commit_chunker.py",
        "multi_commit_summarizer.py",
        "multi_release_formatter_llm.py"
    ]
    for script in scripts:
        print(f"▶️ Running: {script}")
        result = subprocess.run(["python3", script])
        if result.returncode != 0:
            print(f"❌ Error running {script}. Halting.")
            exit(1)

    # Post to Slack
    notes_dir = Path("release_notes")
    md_files = list(notes_dir.glob("*_final.md"))
    if not md_files:
        print("❌ No final release notes found to post.")
        return

    if questionary.confirm("📣 Do you want to post the release notes to Slack?").ask():
        slack_url = os.getenv("SLACK_WEBHOOK_URL") or questionary.text("🌐 Enter Slack Webhook URL:").ask()
        set_key(str(env_file), "SLACK_WEBHOOK_URL", slack_url)
        result = subprocess.run(["python3", "multi_post_release_notes_to_slack.py"])
        if result.returncode != 0:
            print("❌ Error posting to Slack.")
        else:
            print("✅ Release notes posted to Slack!")

    print("\n✅ All done.")

# Entry point for PyPI-installed CLI
if __name__ == "__main__":
    main()
