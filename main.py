"""
Social Media AI Agent — True Agentic Architecture
===================================================
Uses OpenAI Function Calling so the model decides:
  - what tool to call next
  - when enough information is gathered
  - when to ask the human for approval
  - when to stop

Tools available to the agent:
  1. search_trending_topics  — simulate trend awareness
  2. generate_post           — create post for a platform/style
  3. check_content_safety    — AI moderation review
  4. improve_post            — rewrite with specific feedback
  5. save_approved_post      — persist to file
  6. ask_human_approval      — request human decision
  7. get_platform_guidelines — fetch char limits & tone rules
"""

import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memory: persists across the conversation
memory = {
    "session_start": datetime.now().isoformat(),
    "posts_generated": 0,
    "posts_approved": 0,
    "posts_rejected": 0,
    "history": []           # list of {topic, platform, style, post, status}
}

# Tool Definitions (the agent picks these autonomously)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_platform_guidelines",
            "description": "Get character limits, tone rules, and best practices for a social media platform. Call this FIRST before generating any post.",
            "parameters": {
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["twitter", "linkedin", "instagram", "facebook"],
                        "description": "The target social media platform"
                    }
                },
                "required": ["platform"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_trending_topics",
            "description": "Search for trending topics or hashtags related to a subject to make the post more relevant and discoverable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to find trends for"
                    },
                    "platform": {
                        "type": "string",
                        "description": "Platform to find platform-specific trends"
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_post",
            "description": "Generate a social media post. Call get_platform_guidelines first, then optionally search_trending_topics before generating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "The subject of the post"},
                    "platform": {
                        "type": "string",
                        "enum": ["twitter", "linkedin", "instagram", "facebook"]
                    },
                    "style": {
                        "type": "string",
                        "enum": ["casual", "professional", "funny", "informative"],
                        "description": "Writing tone"
                    },
                    "max_chars": {"type": "integer", "description": "Character limit from platform guidelines"},
                    "trending_hashtags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional trending hashtags to incorporate"
                    }
                },
                "required": ["topic", "platform", "style", "max_chars"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_content_safety",
            "description": "Run AI safety and moderation review on a generated post. Always call this before asking for human approval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "post": {"type": "string", "description": "The post content to review"},
                    "platform": {"type": "string", "description": "Platform context for review"}
                },
                "required": ["post", "platform"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "improve_post",
            "description": "Rewrite and improve the post based on specific feedback or failed safety checks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_post": {"type": "string"},
                    "feedback": {"type": "string", "description": "What needs to be improved"},
                    "platform": {"type": "string"},
                    "style": {"type": "string"},
                    "max_chars": {"type": "integer"}
                },
                "required": ["original_post", "feedback", "platform", "style", "max_chars"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ask_human_approval",
            "description": "Show the final post to the human and ask for approval. Only call this after safety check passes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "post": {"type": "string", "description": "The post to show for approval"},
                    "platform": {"type": "string"},
                    "style": {"type": "string"},
                    "safety_status": {"type": "string", "description": "Result from safety check"},
                    "char_count": {"type": "integer"}
                },
                "required": ["post", "platform", "style", "safety_status", "char_count"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_approved_post",
            "description": "Save the human-approved post to file. Only call this if human explicitly approved.",
            "parameters": {
                "type": "object",
                "properties": {
                    "post": {"type": "string"},
                    "topic": {"type": "string"},
                    "platform": {"type": "string"},
                    "style": {"type": "string"}
                },
                "required": ["post", "topic", "platform", "style"]
            }
        }
    }
]

# Tool Implementations

def get_platform_guidelines(platform: str) -> dict:
    """Returns platform-specific rules the agent uses to guide generation."""
    guidelines = {
        "twitter":   {"max_chars": 280,  "tone": "punchy and conversational", "hashtags": "1-3", "emojis": True},
        "linkedin":  {"max_chars": 1300, "tone": "professional and insightful", "hashtags": "3-5", "emojis": False},
        "instagram": {"max_chars": 2200, "tone": "visual and lifestyle-focused", "hashtags": "5-10", "emojis": True},
        "facebook":  {"max_chars": 500,  "tone": "friendly and engaging", "hashtags": "1-2", "emojis": True},
    }
    return guidelines.get(platform, guidelines["twitter"])


def search_trending_topics(topic: str, platform: str = "twitter") -> dict:
    """Simulates a trend search — in production swap this for a real trends API."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Give me 5 trending hashtags and 2 trending angles for the topic '{topic}' on {platform} in 2026. Return JSON: {{\"hashtags\": [...], \"angles\": [...]}}"
        }],
        response_format={"type": "json_object"},
        temperature=0.7
    )
    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"hashtags": [f"#{topic.replace(' ', '')}", "#trending"], "angles": [topic]}


def generate_post(topic: str, platform: str, style: str, max_chars: int,
                  trending_hashtags: list = None) -> dict:
    """Calls OpenAI to write the post."""
    hashtag_hint = f"Consider using some of these trending hashtags: {', '.join(trending_hashtags)}" if trending_hashtags else ""

    system_prompt = f"""You are an expert social media copywriter for {platform}.
Platform rules: max {max_chars} characters, {style} tone.
{hashtag_hint}
Return ONLY the post text — no explanations, no labels."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write a {style} {platform} post about: {topic}"}
        ],
        temperature=0.8,
        max_tokens=400
    )
    post = response.choices[0].message.content.strip()
    memory["posts_generated"] += 1
    return {"post": post, "char_count": len(post), "within_limit": len(post) <= max_chars}


def check_content_safety(post: str, platform: str) -> dict:
    """AI moderation — checks for harmful content, misinformation, spam."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a strict content safety reviewer. Check for: harmful content, hate speech, misinformation, spam, privacy violations, or platform policy violations. Be concise."
            },
            {
                "role": "user",
                "content": f"Review this {platform} post:\n\n\"{post}\"\n\nReply with JSON: {{\"approved\": true/false, \"issues\": [], \"suggestion\": \"...\"}}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=200
    )
    try:
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception:
        return {"approved": True, "issues": [], "suggestion": ""}


def improve_post(original_post: str, feedback: str, platform: str,
                 style: str, max_chars: int) -> dict:
    """Rewrites the post based on feedback — agent calls this autonomously if safety fails."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a social media copywriter. Rewrite the post fixing the issues. Max {max_chars} chars. {style} tone. Return ONLY the improved post."},
            {"role": "user", "content": f"Original post:\n{original_post}\n\nFeedback to fix:\n{feedback}\n\nRewrite it:"}
        ],
        temperature=0.7,
        max_tokens=400
    )
    post = response.choices[0].message.content.strip()
    memory["posts_generated"] += 1
    return {"post": post, "char_count": len(post), "within_limit": len(post) <= max_chars}


def ask_human_approval(post: str, platform: str, style: str,
                        safety_status: str, char_count: int) -> dict:
    """Pauses the agent loop and asks the human. This is the human-in-the-loop gate."""
    print("\n" + "═" * 60)
    print(f"   {platform.upper()}  ·  {style.capitalize()}  ·  {char_count} chars")
    print("═" * 60)
    print(f"\n{post}\n")
    print("═" * 60)
    print(f"  Safety: {safety_status}")
    print("─" * 60)
    print("  1 → Approve & Save")
    print("  2 → Discard")
    print("  3 → Regenerate with feedback")
    print("─" * 60)

    while True:
        choice = input("  Your decision (1/2/3): ").strip()
        if choice == "1":
            return {"decision": "approved", "feedback": ""}
        elif choice == "2":
            return {"decision": "rejected", "feedback": ""}
        elif choice == "3":
            fb = input("  What to improve? → ").strip()
            return {"decision": "regenerate", "feedback": fb}
        print("  Please enter 1, 2, or 3.")


def save_approved_post(post: str, topic: str, platform: str, style: str) -> dict:
    """Saves approved post to file and updates session memory."""
    filepath = "approved_posts.txt"
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"\n{'═'*60}\n")
        f.write(f"Saved     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Topic     : {topic}\n")
        f.write(f"Platform  : {platform}  |  Style: {style}\n")
        f.write(f"Post      :\n{post}\n")

    memory["posts_approved"] += 1
    memory["history"].append({"topic": topic, "platform": platform,
                               "style": style, "post": post, "status": "approved"})
    return {"saved": True, "file": filepath, "total_approved": memory["posts_approved"]}


# Tool dispatcher
def dispatch_tool(name: str, args: dict):
    """Routes tool calls from the agent to the right function."""
    if name == "get_platform_guidelines":    return get_platform_guidelines(**args)
    if name == "search_trending_topics":     return search_trending_topics(**args)
    if name == "generate_post":              return generate_post(**args)
    if name == "check_content_safety":       return check_content_safety(**args)
    if name == "improve_post":               return improve_post(**args)
    if name == "ask_human_approval":         return ask_human_approval(**args)
    if name == "save_approved_post":         return save_approved_post(**args)
    return {"error": f"Unknown tool: {name}"}


# Agent Reasoning Loop
def run_agent(user_request: str):
    """
    Core agentic loop — the model decides what to do next.
    Runs until the model stops calling tools (task complete).
    """
    print(f"\n🤖 Agent thinking...")

    messages = [
        {
            "role": "system",
            "content": """You are an autonomous social media content agent. 

When given a request, you MUST follow this exact workflow by calling tools in order:
1. ALWAYS call get_platform_guidelines first
2. ALWAYS call search_trending_topics to find relevant hashtags  
3. Call generate_post using the guidelines and trends
4. ALWAYS call check_content_safety on the generated post
5. If safety check fails → call improve_post to fix issues, then re-check safety
6. If safety check passes → call ask_human_approval
7. If human approves → call save_approved_post
8. If human wants regeneration → call improve_post with their feedback, then repeat from step 4
9. If human rejects → stop and confirm discarded

Never skip steps. Never ask the user what to do next — decide autonomously using the tools.
Be efficient: complete the full workflow without unnecessary steps."""
        },
        {"role": "user", "content": user_request}
    ]

    iteration = 0
    max_iterations = 15  # safety guard against infinite loops

    while iteration < max_iterations:
        iteration += 1

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.7
        )

        msg = response.choices[0].message

        # No more tool calls → agent is done
        if not msg.tool_calls:
            if msg.content:
                print(f"\n {msg.content}")
            break

        # Process all tool calls the agent decided to make
        messages.append(msg)

        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"  ⚙️  Agent calling: {tool_name}({', '.join(f'{k}={repr(v)}' for k,v in tool_args.items())})")

            result = dispatch_tool(tool_name, tool_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    if iteration >= max_iterations:
        print("  Agent reached max iterations — stopping.")

    return memory


# Session summary 
def print_session_summary():
    print("\n" + "═" * 60)
    print("   Session Summary")
    print("─" * 60)
    print(f"  Posts generated : {memory['posts_generated']}")
    print(f"  Posts approved  : {memory['posts_approved']}")
    print(f"  Posts rejected  : {memory['posts_rejected']}")
    if memory["history"]:
        print(f"\n  Approved posts saved to: approved_posts.txt")
    print("═" * 60)


# Main CLI 
def main():
    print("═" * 60)
    print("  🤖 Social Media AI Agent  (Agentic Mode)")
    print("═" * 60)
    print("  The agent autonomously plans, generates, moderates,")
    print("  and only stops to ask YOU for final approval.")
    print()
    print("  Example: 'Write a LinkedIn post about AI in healthcare'")
    print("  Example: 'Create a funny Twitter post about Python bugs'")
    print("  Example: 'Instagram post about my startup launch'")
    print("─" * 60)

    while True:
        print()
        request = input("  Your request (or 'quit' to exit):\n  → ").strip()

        if not request:
            continue

        if request.lower() in ("quit", "exit", "q"):
            print_session_summary()
            print("\n  Goodbye! \n")
            break

        run_agent(request)


if __name__ == "__main__":
    main()
