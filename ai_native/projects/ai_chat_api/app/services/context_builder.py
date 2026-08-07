# history
# memories
# message
#         │
#         ▼

# ① Build System Prompt

#         │
#         ▼


# ② Inject Memories
#         │
#         ▼
# ③ Append Conversation History
#         │
#         ▼
# ④ Append Current User Message
#         │
#         ▼
# messages gửi cho Ollama
from app.prompts.system_context_prompt import build_system_context_prompt
from app.schemas.memory_schema import Memory


class ContextBuilder:
    max_context_messages = 20

    def __init__(self):
        pass

    def _format_memories(self, memories: list[Memory]) -> str:
        if not memories:
            return ""
        return "\n".join([f"- {memory.content}" for memory in memories])

    def build(
        self, history: list[dict[str, str]], memories: list, user_message: str = ""
    ) -> list[dict[str, str]]:
        context = history.copy()
        context.append({"role": "user", "content": user_message})

        memories_copy = memories.copy() if memories else []

        known_facts = self._format_memories(memories_copy)

        system_prompt = {
            "role": "system",
            "content": build_system_context_prompt(known_facts),
        }

        return [
            system_prompt,
            *context[-self.max_context_messages :],
        ]


# - Tên người dùng là Nhất
# - Đang học AI Backend
# - Thích Python
