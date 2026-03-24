# Social Media AI Agent

An AI-powered command-line tool that generates social media posts on any topic, reviews them for safety, and saves approved content all with human approval at every step.

## Features

- Generate posts on any topic in seconds
- Choose from 4 writing styles: Casual, Professional, Funny, or Informative
- Built-in AI safety check before you approve
- Approve, discard, or regenerate with a single keystroke
- Saves all approved posts to a local file with timestamps

---

## Requirements

- Python 3.9+
- An OpenAI API key with available credits

---

## Installation

**1. Clone the repository**

```bash
git clone copy this project url
cd social-media-agent
```

**2. Install dependencies using uv**

```bash
uv add python-dotenv openai
```

Or using pip:

```bash
pip install python-dotenv openai
```

**3. Set up your environment variables**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

---

## Usage

Run the agent:

```bash
python social_media_agent.py
```

### Example Session

```
============================================================
  Social Media AI Agent
============================================================

------------------------------------------------------------
Enter a topic (or 'quit' to exit): Coffee

Choose a writing style:
  1. Casual
  2. Professional
  3. Funny
  4. Informative

Enter 1-4: 3

🤖 Generating post...

============================================================
☕️ Coffee: because adulting is hard and sleep is for the weak! 💤
Who needs a superhero when you have a cup of joe that can transform
you from a zombie to a functioning human? 🦸 Let's raise our mugs
to caffeine and the magic it brings! #BrewtifulLife #CaffeineQueen #JavaJive
============================================================
Characters: 277

🔍 Running safety check...
✅ Looks good

  1. Approve and save
  2. Discard
  3. Regenerate

Enter 1-3: 1
✅ Saved to approved_posts.txt
```

---

## Writing Styles

| Style | Description |
|---|---|
| **Casual** | Friendly and conversational |
| **Professional** | Business-like and polished |
| **Funny** | Humorous and entertaining |
| **Informative** | Educational and factual |

---

## Output

Approved posts are saved to `approved_posts.txt` in the project root with the following format:

```
============================================================
Timestamp: 2025-03-24 14:32:10
Topic: Coffee
Post: ☕️ Coffee: because adulting is hard and sleep is for the weak!...
```

---

## Project Structure

```
social-media-agent/
│
├── social_media_agent.py   # Main application
├── approved_posts.txt      # Saved approved posts (auto-created)
├── .env                    # API key (not committed to git)
├── .gitignore
└── README.md
```

---

## Safety & Ethics

Every generated post goes through an automated AI content review before you see the approval prompt. The review checks for:

- Offensive or harmful content
- Misinformation
- Promotional spam
- Privacy violations

You remain in full control — nothing is saved without your explicit approval.

---

## .gitignore Recommendation

Make sure your `.env` file is never committed:

```
.env
approved_posts.txt
__pycache__/
.venv/
```

---

## License

MIT License — free to use, modify, and distribute.
