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
from app.schemas.memory_rerank_schema import MemoryRerankResult
from app.services.token_counter import TokenCounter
import numpy as np


class ContextBuilder:
    max_context_messages = 20

    def __init__(
        self,
        token_counter: TokenCounter,
        max_retrieved_context_tokens: int = 3000,
        semantic_dedup_threshold: float = 0.90,
    ):
        self.token_counter = token_counter
        self.max_retrieved_context_tokens = max_retrieved_context_tokens
        self.semantic_dedup_threshold = semantic_dedup_threshold

    def _format_memories(self, memories: list[MemoryRerankResult]) -> str:
        if not memories:
            return ""
        return "\n".join([f"- {memory.memory.content}" for memory in memories])

    def _cosine_similarity(
        self,
        a: list[float],
        b: list[float],
    ) -> float:
        if len(a) != len(b):
            raise ValueError("Vectors must have the same dimension")
        vector_a = np.asarray(a, dtype=np.float32)
        vector_b = np.asarray(b, dtype=np.float32)

        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)

        if norm_a == 0 or norm_b == 0:
            raise ValueError("Cannot calculate cosine similarity " "for zero vector")

        return float(np.dot(vector_a, vector_b) / (norm_a * norm_b))

    def _deduplicate_memories(
        self,
        memories: list[MemoryRerankResult],
    ) -> list[MemoryRerankResult]:

        if not memories:
            return []

        selected: list[MemoryRerankResult] = []

        for current in memories:
            is_duplicate = False
            current_embedding = current.memory.embedding

            for existing in selected:
                existing_embedding = existing.memory.embedding

                if current_embedding is None:
                    raise ValueError("Memory embedding is required")

                if existing_embedding is None:
                    raise ValueError("Memory embedding is required")

                similarity = self._cosine_similarity(
                    current.memory.embedding,
                    existing.memory.embedding,
                )

                if similarity >= self.semantic_dedup_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                selected.append(current)

        return selected

    def _fit_to_token_budget(
        self,
        memories: list[MemoryRerankResult],
    ) -> list[MemoryRerankResult]:
        selected = []
        total_tokens = 0

        for item in memories:
            tokens = self.token_counter.count(item.memory.content)

            if total_tokens + tokens > self.max_retrieved_context_tokens:
                continue

            selected.append(item)
            total_tokens += tokens

        return selected

    def build(
        self,
        history: list[dict[str, str]],
        memories: list[MemoryRerankResult],
        user_message: str = "",
    ) -> list[dict[str, str]]:
        context = history.copy()
        context.append({"role": "user", "content": user_message})

        selected_memories = self._deduplicate_memories(memories)

        selected_memories = self._fit_to_token_budget(selected_memories)

        known_facts = self._format_memories(selected_memories)

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
