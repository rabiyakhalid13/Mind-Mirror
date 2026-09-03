import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# ---- Safety response for crisis cases (no AI generation - fixed, reliable) ----
CRISIS_RESPONSE = """I hear that you're going through something really painful right now, and I want you to know that you're not alone in this.

What you're feeling matters, and it's important to talk to someone who can support you properly right now.

**Please reach out:**
- Umang Pakistan Helpline: 0311-7786264
- Talk to a trusted friend, family member, or counselor

You don't have to go through this by yourself. Reaching out for help is a sign of strength, not weakness."""


def build_system_prompt(pattern_insights):
    """Build a context-aware system prompt using pattern insights"""

    context_notes = ""
    if pattern_insights and "message" not in pattern_insights:
        worst_day = pattern_insights.get("worst_day")
        trend = pattern_insights.get("trend")

        if worst_day:
            context_notes += f"- The user's mood tends to be lowest on {worst_day}s.\n"
        if trend == "declining":
            context_notes += "- The user's mood has been declining over the past week.\n"
        elif trend == "improving":
            context_notes += "- The user's mood has been improving over the past week.\n"

    system_prompt = f"""You are MindMirror, a supportive AI journaling companion. Your role is NOT to act as a therapist, but to help users reflect on their emotions using gentle, CBT-inspired techniques.
Guidelines:
- Keep responses short (3-5 sentences max), warm, and conversational.
- Use gentle CBT-style reframing when appropriate (help identify unhelpful thought patterns, without being preachy).
- If pattern context is provided below, reference it naturally to show the user you understand their history — but do not sound robotic or clinical.
- End with ONE small, actionable suggestion (a micro-action, not generic advice like "stay positive").
- Never diagnose. Never claim to be a medical professional. Never use clinical labels (e.g. depression, anxiety disorder).
- Do not be overly cheerful if the user is struggling — match their emotional tone with empathy first.

{"User pattern context:" if context_notes else ""}
{context_notes}
"""
    return system_prompt


def get_agent_response(statement, mood_category, pattern_insights=None):
    """
    Main function: takes journal statement + predicted mood + pattern insights,
    returns an appropriate agent response.
    """

    # Safety-first: crisis case gets a fixed, reliable response (not AI-generated)
    if mood_category == "You're not Alone":
        return CRISIS_RESPONSE

    system_prompt = build_system_prompt(pattern_insights)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Journal entry: \"{statement}\"\nDetected mood: {mood_category}\n\nRespond supportively.")
    ]

    response = llm.invoke(messages)
    if isinstance(response.content, str):
        return response.content
    elif isinstance(response.content, list):
        # Extract text from list of blocks
        text_parts = [block.get('text', '') for block in response.content if isinstance(block, dict)]
        return ' '.join(text_parts).strip()
    else:
        return str(response.content)


# ---- Test ----
if __name__ == "__main__":
    test_statement = input("Enter a journal entry to test the agent: ")
    test_mood = input("Enter mood category to simulate (Feeling Good / A Bit Overwhelmed / Going Through a Tough Time / You're not Alone): ")

    dummy_insights = {"worst_day": "Monday", "trend": "declining"}

    response = get_agent_response(test_statement, test_mood, dummy_insights)
    print("\n--- Agent Response ---")
    print(response)