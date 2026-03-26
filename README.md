# 🤖 Social Media AI Agent

An autonomous AI agent that **plans, generates, moderates, and saves** social media content — stopping only when it needs your final approval.

Built with **OpenAI GPT-4o-mini Function Calling** and Python — this is a true agentic system where the model decides what to do next, not hardcoded `if/else` logic.

---

## 🎯 Real Output

```
════════════════════════════════════════════════════════════
  🤖 Social Media AI Agent  (Agentic Mode)
════════════════════════════════════════════════════════════
  The agent autonomously plans, generates, moderates,
  and only stops to ask YOU for final approval.
────────────────────────────────────────────────────────────

  → Create a funny post about AI in Gym

🤖 Agent thinking...
  ⚙️  Agent calling: get_platform_guidelines(platform='twitter')
  ⚙️  Agent calling: search_trending_topics(topic='AI', platform='twitter')
  ⚙️  Agent calling: generate_post(topic='AI in Gym', style='funny', max_chars=280)
  ⚙️  Agent calling: check_content_safety(post='...', platform='twitter')
  ⚙️  Agent calling: ask_human_approval(safety_status='approved', char_count=170)

════════════════════════════════════════════════════════════
  📱 TWITTER  ·  Funny  ·  170 chars
════════════════════════════════════════════════════════════

  Just walked into the gym and my AI personal trainer asked
  if I wanted a workout or a nap. I mean, who knew machines
  could read my mind? 😂💪 #AIRevolution #GymLife #NapTime

════════════════════════════════════════════════════════════
  Safety: approved
  1 → Approve & Save  |  2 → Discard  |  3 → Regenerate
────────────────────────────────────────────────────────────
  Your decision: 1
  ⚙️  Agent calling: save_approved_post(...)

✅ Post saved successfully!
```

---

## 🔧 Agent Tools

The agent autonomously picks and chains these tools in the right order:

```
1. get_platform_guidelines   → character limits, tone rules per platform
2. search_trending_topics    → relevant hashtags and trending angles
3. generate_post             → writes the post using OpenAI
4. check_content_safety      → AI moderation review
5. improve_post              → auto-rewrites if safety check fails
6. ask_human_approval        → human-in-the-loop gate before saving
7. save_approved_post        → saves to file with metadata
```

---

## 🔄 Agent Workflow

```
User Request
     │
     ▼
┌─────────────────────────────────┐
│      Agent Reasoning Loop       │
│  GPT-4o-mini + Function Calling │
└────────────────┬────────────────┘
                 │  decides tool order autonomously
     ┌───────────┼──────────────────────┐
     ▼           ▼           ▼          ▼
 Platform    Trending    Generate    Safety
 Guidelines   Topics       Post       Check
                             │           │
                             │     fail? → improve_post → re-check
                             │           │
                             └─────────► Ask Human
                                         │
                               ┌─────────┼──────────┐
                               ▼         ▼          ▼
                            Approve   Reject    Regenerate
                               │                   │
                               ▼                   └──► improve_post → loop
                          Save to File
```

---

## 📱 Supported Platforms

| Platform | Max Chars | Tone | Hashtags |
|---|---|---|---|
| Twitter | 280 | Punchy, conversational | 1–3 |
| LinkedIn | 1300 | Professional, insightful | 3–5 |
| Instagram | 2200 | Visual, lifestyle | 5–10 |
| Facebook | 500 | Friendly, engaging | 1–2 |

---

## 🚀 Setup & Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Create `.env` file**
```
OPENAI_API_KEY=your_openai_key_here
```

**3. Run the agent**
```bash
python agent.py
```

---

## 💬 Example Requests

```
→ Write a LinkedIn post about AI in healthcare
→ Create a funny Twitter post about Python bugs
→ Instagram post about my startup launch
→ Professional Facebook post about remote work trends
→ Create a funny post about AI in Gym
```

---

## 📊 Session Summary

At the end of each session the agent reports:

```
════════════════════════════════════════════════════════════
  📊 Session Summary
────────────────────────────────────────────────────────────
  Posts generated : 3
  Posts approved  : 2
  Posts rejected  : 1
  Approved posts saved to: approved_posts.txt
════════════════════════════════════════════════════════════
```

All approved posts are saved to `approved_posts.txt` with timestamp, topic, platform, and style metadata.

---

## 📁 Project Structure

```
social_agent/
├── agent.py            # Main agent — reasoning loop + all tools
├── requirements.txt    # Dependencies
├── .env                # Your OpenAI API key (not committed)
├── approved_posts.txt  # Auto-created when first post is approved
└── README.md
```

---

## 🛡️ Responsible AI Practices

- **Human-in-the-loop**: No post is ever saved without explicit human approval
- **AI content moderation**: Every post passes a safety check before reaching you
- **Auto-repair**: If moderation flags issues, the agent rewrites and re-checks automatically
- **Transparency**: Every tool call is printed so you see exactly what the agent is doing

---

## 📝 Tech Stack

- **Python 3.10+**
- **OpenAI GPT-4o-mini** — generation, safety review, trend search
- **OpenAI Function Calling** — autonomous tool selection and chaining
- **python-dotenv** — environment variable management

---

## 🔗 Repository

**GitHub:** [github.com/RameshPrabakar/social-media-agent](https://github.com/RameshPrabakar/social-media-agent)
