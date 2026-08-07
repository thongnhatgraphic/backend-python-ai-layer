# Business Rules
# ↓
# Prompt
from app.prompts.rules.memory_rules import LONG_TERM_MEMORY_RULES


def build_memory_score_prompt(
    conversation_format: str,
    memories_extrator_format: str,
    extra_rules: str = "",
) -> str:
    return f"""
    Your are an AI professional memory scoring assistant.
    Score between 0.0 and 1.0.
    
    This is the current context of conversation: {conversation_format}
    this is the memories extracted: {memories_extrator_format}

    Your ONLY task is to score the quality of the memories.
    You will evaluate the quality of the memories and score it.
    Score only facts that are useful in future conversations.
    Evaluate EACH memory independently.
    If a memory is inconsistent with the conversation,
    you should give it a very low score.
    Return ONE score for EACH extracted memory.

    {LONG_TERM_MEMORY_RULES}

    You are NOT a chatbot.
    You MUST NOT answer the user's questions.
    You MUST NOT continue the conversation.
    {extra_rules}
    
    Return ONLY a JSON array.
    Schema:
    example: [
        {{
            "content": "...",
            "score": 0.5
        }},
    ]

    
"""


# 👍 Điểm 1 - Role
# Your are an AI professional memory scoring assistant.

# 👍 Điểm 2 - Có giới hạn nhiệm vụ
# You are NOT a chatbot.
# You MUST NOT answer...

# 👍 Điểm 3 - Tiêu Chí đánh giá
# You MUST NOT continue the conversation.
# Higher score means:
# - Stable over time.
# - Useful in future conversations.
# - Represents user's identity.
# - Represents long-term preference.
# - Represents long-term goals.
# Lower score means:

# - Temporary events.
# - Greetings.
# - Small talk.
# - Weather.
# - One-time requests.
