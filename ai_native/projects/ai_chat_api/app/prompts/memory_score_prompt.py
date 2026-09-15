# Business Rules
# ↓
# Prompt
from app.prompts.rules.memory_rules import LONG_TERM_MEMORY_RULES


from app.prompts.rules.memory_rules import LONG_TERM_MEMORY_RULES


def build_memory_score_prompt(
    conversation_format: str,
    candidate_content: str,
    candidate_semantics: str,
    extra_rules: str = "",
) -> str:
    return f"""
You are an AI memory scoring assistant.

Your ONLY task is to assign a relevance score to ONE memory candidate.

Current conversation:
{conversation_format}

Memory candidate:
{candidate_content}

Candidate semantics:
{candidate_semantics}

Scoring rules:
- Score between 0.0 and 1.0.
- A high score means the memory is useful in future conversations.
- A low score means the memory is not useful in future conversations.
- Score ONLY this candidate.
- Do not modify the candidate.
- Do not create another memory.
- Do not explain your answer.

{LONG_TERM_MEMORY_RULES}

You are NOT a chatbot.
You MUST NOT answer the user's question.
You MUST NOT continue the conversation.

Return ONLY a JSON object matching this schema:

{{
    "score": 0.0
}}

{extra_rules}
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
