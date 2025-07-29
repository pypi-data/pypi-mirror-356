#!/usr/bin/env python3.13
"""
multi_release_user_note_llm.py

Takes summaries/{repo}.md → user_release_notes/{repo}_user.md
"""
import os
from pathlib import Path
from dotenv import load_dotenv; load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))

SUMMARY_DIR = Path("summaries")
USER_DIR = Path("user_release_notes"); USER_DIR.mkdir(exist_ok=True)

for summary_file in sorted(SUMMARY_DIR.glob("*.md")):
    repo = summary_file.stem
    print(f"\n🧠 Writing user-friendly release note for: {repo}")
    raw = summary_file.read_text()

    PROMPT = f"""
You are a product marketer writing a release note for end users — not for developers.

Here's the internal changelog:
{raw}

🧠 Convert it into a **friendly, simple, and user-facing release note**.
Avoid tech jargon. Instead, focus on what this update enables users to do, what gets easier, and how it improves their daily experience.

🎯 Guidelines:
- DO NOT use dev/infra terms like CRUD, endpoints, or APIs
- Group multiple related updates into broader benefits
- Use plain English. Assume the reader is *not* a developer
- Keep it light, clear, and motivational — like a Notion or Slack changelog
- Use emoji ✨ and bold Markdown to highlight sections
- Max 2–3 sections: What’s New, What It Means for You, Thank You

🧩 Use this structure:

🚀 **What’s New**  
Summarize the biggest changes users will actually notice. Write them as capabilities.

💡 **What This Means for You**  
Explain how this helps users — smoother workflows, better speed, or more control.


Return only clean Markdown.
"""
    try:
        response = model.generate_content(PROMPT)
        output_path = USER_DIR / f"{repo}_user.md"
        output_path.write_text(response.text.strip())
        print(f"✅ User note saved ➜ {output_path.resolve()}")
    except Exception as e:
        print(f"❌ Error creating user note for {repo}: {e}")
