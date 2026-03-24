# Social Media AI Agent with Approval

This repository contains a small Python-based AI assistant that generates social media posts and requires human approval before saving.

## Features

- Generate social media post drafts from a topic and style.
- Supports styles: casual, professional, funny, informative.
- Safety review via OpenAI moderation-style prompt.
- User approval flow (approve/save, reject, regenerate).
- Save approved posts to approved_posts.txt with timestamp and topic.

## Requirements

- Python 3.14+
- python-dotenv
- openai
- python-frontmatter (not required by project/main.py, but in project deps)
- 
equests (in dependencies)

## Setup

1. Create and activate your venv:

`powershell
cd project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
`

2. Install dependencies:

`powershell
pip install -r requirements.txt  # if you have it, or:
uv sync
`

3. Add env file .env in project/ with:

`dotenv
OPENAI_API_KEY=sk-...
`

4. Make sure .env is loaded by load_dotenv() in main.py.

## Usage

`powershell
cd project
.\.venv\Scripts\Activate.ps1
python main.py
`

Follow prompts:
- type topic
- choose style
- approve/reject/regenerate

Approved posts are appended to approved_posts.txt.

## main.py workflow

1. load_dotenv() reads .env values.
2. OpenAI(api_key=...) initializes client.
3. generate_social_post(topic, style) creates prompt and calls chat.completions.create.
4. 
eview_post(post_text) calls OpenAI to validate for content policy issues.
5. save_approved_post(post_text, topic) writes approved posts to file.
6. main() loops until user exits.

## Common issues

- ModuleNotFoundError: No module named 'dotenv': install python-dotenv.
- insufficient_quota / 429: update OpenAI billing or plan.
- OPENAI_API_KEY missing: define in .env and export.

## Notes

- Protect your API key; do not commit .env to git.
- The script uses Chat Completions API with gpt-3.5-turbo and max_tokens=200.
- Adjust max_length, 	emperature, or safety prompt in functions as needed.
