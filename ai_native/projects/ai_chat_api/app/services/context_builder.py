#                 ContextBudget
#                      │
#                28,160 tokens
#                      │
#                      ▼
#              ContextBuilder
#                      │
#     ┌────────────────┼─────────────────┐
#     ↓                ↓                 ↓
#   Memory             RAG             History
#     │                │                 │
#     └────────────────┼─────────────────┘
#                      ↓
#               ContextUsage
#                      │
#                      ▼
#               total_tokens
#                      │
#                      ▼
#              remaining_budget


from app.prompts.system_context_prompt import build_system_context_prompt
from app.schemas.memory_rerank_schema import MemoryRerankResult
from app.schemas.retrieval_schema import RetrievalResult
from app.schemas.context_schemas.context_usage import ContextUsage
from app.schemas.context_schemas.context_candidate import ContextCandidate
from app.schemas.context_schemas.context_plan import ContextPlan
from app.schemas.context_schemas.context_allocation import ContextAllocation

from app.services.token_counter import TokenCounter

from app.context.context_budget import ContextBudget
from app.context.context_priority import ContextImportance

from app.core.settings import settings

import numpy as np


class ContextBuilder:
    max_context_messages = 20

    def __init__(
        self,
        token_counter: TokenCounter,
        context_budget: ContextBudget,
        semantic_dedup_threshold: float = 0.90,
    ):
        self.token_counter = token_counter
        self.context_budget = context_budget

        self.semantic_dedup_threshold = semantic_dedup_threshold

    def _measure_context_usage(
        self,
        history: list[dict[str, str]],
        user_message: str,
        memory_context: str,
        retrieved_context: str,
    ) -> ContextUsage:

        system_instruction = build_system_context_prompt("")

        return ContextUsage(
            system_tokens=self.token_counter.count(system_instruction),
            memory_tokens=self.token_counter.count(memory_context),
            rag_tokens=self.token_counter.count(retrieved_context),
            history_tokens=sum(
                [
                    self.token_counter.count(f"{message['role']}: {message['content']}")
                    for message in history
                ]
            ),
            user_tokens=self.token_counter.count(user_message),
        )

    def _format_memories(self, memories: list[MemoryRerankResult]) -> str:
        if not memories:
            return ""
        return "\n".join([f"- {memory.memory.content}" for memory in memories])

    def _format_documents(self, documents: list[RetrievalResult]) -> str:
        if not documents:
            return ""
        return "\n\n".join(
            [
                (
                    f"[Document {index}]\n"
                    f"Source: {document.external_id}\n"
                    f"Title: {document.title}\n"
                    f"Content: {document.content}"
                )
                for index, document in enumerate(documents, start=1)
            ]
        )

    def _format_history(self, history: list[dict[str, str]]) -> str:
        return "\n".join(
            [f"{message['role']}: {message['content']}" for message in history]
        )

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

    def _fit_memories_to_token_budget(
        self,
        memories: list[MemoryRerankResult],
        budget: int,
    ) -> list[MemoryRerankResult]:
        if budget <= 0:
            return []

        selected = []
        used_tokens = 0

        for memory in memories:

            text = memory.memory.content
            tokens = self.token_counter.count(text)

            if used_tokens + tokens > budget:
                break

            selected.append(memory)
            used_tokens += tokens

        return selected

    def _fit_documents_to_token_budget(
        self,
        documents: list[RetrievalResult],
        budget: int,
    ) -> list[RetrievalResult]:
        if budget <= 0:
            return []

        selected = []
        used_tokens = 0

        for index, document in enumerate(documents, start=1):
            text = (
                f"[Document {index}]\n"
                f"Source: {document.external_id}\n"
                f"Title: {document.title}\n"
                f"Content: {document.content}"
            )

            tokens = self.token_counter.count(text)

            if used_tokens + tokens > budget:
                break

            selected.append(document)
            used_tokens += tokens

        return selected

    def build_context_candidates(
        self,
        plan: ContextPlan,
        memories: list[MemoryRerankResult],
        retrieved_documents: list[RetrievalResult],
        history: list[dict[str, str]],
    ) -> list[ContextCandidate]:
        memory_context = self._format_memories(memories)

        rag_context = self._format_documents(retrieved_documents)

        history_text = self._format_history(history)

        return [
            ContextCandidate(
                name="memory",
                demand_tokens=(
                    self.token_counter.count(memory_context)
                    if plan.memory.importance != ContextImportance.NONE
                    else 0
                ),
                max_tokens=settings.CONTEXT_MEMORY_MAX_USEFUL_TOKENS,
                priority=plan.memory.importance,
            ),
            ContextCandidate(
                name="rag",
                demand_tokens=(
                    self.token_counter.count(rag_context)
                    if plan.rag.importance != ContextImportance.NONE
                    else 0
                ),
                max_tokens=settings.CONTEXT_RAG_MAX_USEFUL_TOKENS,
                priority=plan.rag.importance,
            ),
            ContextCandidate(
                name="history",
                demand_tokens=(
                    self.token_counter.count(history_text)
                    if plan.history.importance != ContextImportance.NONE
                    else 0
                ),
                max_tokens=settings.CONTEXT_HISTORY_MAX_USEFUL_TOKENS,
                priority=plan.history.importance,
            ),
        ]

    def _fit_history_to_token_budget(
        self,
        history: list[dict[str, str]],
        budget: int,
    ) -> list[dict[str, str]]:
        if budget <= 0:
            return []

        selected = []
        used_tokens = 0

        for message in reversed(history):

            text = f"{message['role']}: {message['content']}"
            tokens = self.token_counter.count(text)

            if used_tokens + tokens > budget:
                break

            selected.append(message)
            used_tokens += tokens

        selected.reverse()

        return selected

    def build(
        self,
        history: list[dict[str, str]],
        memories: list[MemoryRerankResult],
        retrieved_documents: list[RetrievalResult],
        allocation: ContextAllocation,
        user_message: str = "",
    ) -> list[dict[str, str]]:

        # ---------------------------------------------------------
        # 1. Memory
        # ---------------------------------------------------------
        selected_memories = self._deduplicate_memories(memories)

        selected_memories = self._fit_memories_to_token_budget(
            selected_memories,
            allocation.memory_tokens,
        )

        known_facts = self._format_memories(selected_memories)

        # ---------------------------------------------------------
        # 2. RAG
        # ---------------------------------------------------------
        selected_documents = self._fit_documents_to_token_budget(
            retrieved_documents,
            allocation.rag_tokens,
        )

        retrieved_context = self._format_documents(selected_documents)

        # ---------------------------------------------------------
        # 3. History
        # ---------------------------------------------------------
        selected_history = self._fit_history_to_token_budget(
            history,
            allocation.history_tokens,
        )

        # Respect the message-count guardrail.
        selected_history = selected_history[-self.max_context_messages :]

        # ---------------------------------------------------------
        # 4. System prompt
        # ---------------------------------------------------------
        system_prompt = {
            "role": "system",
            "content": (
                build_system_context_prompt(known_facts)
                + "\n\n"
                + "Retrieved knowledge:\n"
                + retrieved_context
            ),
        }

        # ---------------------------------------------------------
        # 5. Final conversation context
        # ---------------------------------------------------------
        context = [
            *selected_history,
            {
                "role": "user",
                "content": user_message,
            },
        ]

        # ---------------------------------------------------------
        # 6. Measure ACTUAL context usage
        # ---------------------------------------------------------
        usage = self._measure_context_usage(
            history=selected_history,
            user_message=user_message,
            memory_context=known_facts,
            retrieved_context=retrieved_context,
        )

        print("\n===== CONTEXT USAGE =====")
        print("system:", usage.system_tokens)
        print("memory:", usage.memory_tokens)
        print("rag:", usage.rag_tokens)
        print("history:", usage.history_tokens)
        print("user:", usage.user_tokens)
        print("total:", usage.total_tokens)
        print("budget:", self.context_budget.max_input_tokens)
        print(
            "remaining:",
            self.context_budget.max_input_tokens - usage.total_tokens,
        )

        return [
            system_prompt,
            *context,
        ]


# - Tên người dùng là Nhất
# - Đang học AI Backend
# - Thích Python
