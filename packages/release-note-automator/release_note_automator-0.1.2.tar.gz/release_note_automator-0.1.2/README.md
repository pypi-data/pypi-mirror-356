# Release Note Automator

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

**Release Note Automator** is a command-line tool that fetches, cleans, summarizes, and posts structured release notes from Azure DevOps repositories. Powered by Google Gemini and designed to streamline DevOps communication.

---

## ✨ Features

- 🔄 Fetch commits from multiple Azure DevOps repos
- 🧹 Clean noisy commit messages
- 🧠 Summarize using Gemini API
- 🗂️ Format clean markdown release notes
- 📤 Optional Slack integration for posting notes
- ✅ Interactive CLI workflow
- 📦 Packaged for pip and PyPI

---

## 📦 Installation

```bash
pip install release-note-automator
```

Or from source:

```bash
git clone https://github.com/ankur-helak/release-note-automator.git
cd release-note-automator
pip install .
```
## 🚀 Usage
```bash
rlauto
```
The CLI will guide you through:

Entering Azure DevOps org, project, and PAT

Entering Gemini API key

Selecting repositories

Selecting how many days of commit history to consider

Running the release note generation pipeline

Optionally posting notes to Slack

## 🧠 Requirements
Python 3.8+

Valid Azure DevOps Personal Access Token (PAT)

Google Gemini API key (from Google AI Studio)

Optional Slack Webhook URL

## 📁 Output
commits/: Raw commit logs

cleaned_commits/: Cleaned and filtered messages

chunks/: Chunked text files for summarization

summaries/: Gemini-based text summaries

release_notes/: Final Markdown release notes

## 📄 Example
```bash
✅ design-studio-backend → SHA: 75a3f88 (starting from: 02 Jun 2025)
✅ design-studio-frontend → SHA: d4bb2d7 (starting from: 02 Jun 2025)

🚀 Running release note pipeline …
✅ Final note saved ➜ release_notes/design-studio-backend_final.md
✅ Final note saved ➜ release_notes/design-studio-frontend_final.md

📣 Do you want to post the release notes to Slack? Yes
✅ Release notes posted to Slack!
```

## 🤝 Contributing
Contributions, issues and feature requests are welcome!
Feel free to open an issue.

## 🛡 License
This project is licensed under the terms of the MIT license.

## 🙋‍♂️ Author
Ankur Helak – @ankur-helak
Email: ankurhelak@gmail.com