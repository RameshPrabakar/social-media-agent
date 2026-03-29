import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


STYLES = {
    "1": ("casual",       "Write in a friendly, conversational tone"),
    "2": ("professional", "Write in a professional, business tone"),
    "3": ("funny",        "Write in a humorous, entertaining tone"),
    "4": ("informative",  "Write in an educational, informative tone"),
}


def generate_post(topic, style_instruction, max_length=280):
    prompt = f"""Create a social media post about: {topic}

Requirements:
- {style_instruction}
- Maximum {max_length} characters
- Engaging and attention-grabbing
- Include 1-3 relevant hashtags
- Emojis are fine if appropriate

Return only the post text, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def is_post_safe(post):
    prompt = f"""Review this social media post for issues:

"{post}"

Check for offensive content, misinformation, spam, or privacy violations.
If it's fine, reply with just "APPROVED". Otherwise list the concerns."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a content moderator focused on safety and ethics."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=150
    )

    result = response.choices[0].message.content.strip()
    approved = "APPROVED" in result.upper()
    return approved, [] if approved else [result]


def save_post(post, topic):
    with open("approved_posts.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Topic: {topic}\n")
        f.write(f"Post:\n{post}\n")


def pick_style():
    print("\nChoose a writing style:")
    for key, (name, _) in STYLES.items():
        print(f"  {key}. {name.capitalize()}")

    while True:
        choice = input("\nEnter 1-4: ").strip()
        if choice in STYLES:
            return STYLES[choice]
        print("Please enter a number between 1 and 4.")


def main():
    print("=" * 60)
    print("  Social Media AI Agent")
    print("=" * 60)
    print()
    print("This AI helps you create social media posts.")
    print("You'll review and approve each post before saving.")
    print()
    
    while True:
        print("\n" + "-" * 60)
        topic = input("\nEnter a topic (or 'quit' to exit): ").strip()

        if topic.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break

        if not topic:
            continue

        style_name, style_instruction = pick_style()

        while True:
            print("\n🤖 Generating post...")

            try:
                post = generate_post(topic, style_instruction)
            except Exception as e:
                print(f"\n❌ Error: {e}")
                break

            print(f"\n{'='*60}")
            print(post)
            print(f"{'='*60}")
            print(f"Characters: {len(post)}")

            print("\n🔍 Running safety check...")
            safe, issues = is_post_safe(post)

            if not safe:
                print("\n⚠️  Issues found:")
                for issue in issues:
                    print(f"  • {issue}")
            else:
                print("✅ Looks good")

            print("\n  1. Approve and save")
            print("  2. Discard")
            print("  3. Regenerate")

            while True:
                decision = input("\nEnter 1-3: ").strip()
                if decision in ("1", "2", "3"):
                    break
                print("Please enter 1, 2, or 3.")

            if decision == "1":
                save_post(post, topic)
                print("\n✅ Saved to approved_posts.txt")
                break
            elif decision == "2":
                print("\n🗑️  Discarded")
                break
            # decision == "3" → loop again and regenerate


if __name__ == "__main__":
    main()
