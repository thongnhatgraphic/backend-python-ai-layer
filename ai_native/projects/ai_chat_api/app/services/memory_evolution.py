# MemoryEvolution                            │
#      │                                     │
#      ├─ for each new memory                │
#      │                                     │
#      ├─ Candidate Retrieval                │
#      │       │                             │
#      │       └── MemoryStore.search()      │
#      │                                     │
#      ├─ Decision Engine                    │
#      │       │                             │
#      │       ▼                             │
#      │  INSERT / DUPLICATE                 │
#      │  MERGE / UPDATE                     │
#      │                                     │
#      ├─ if MERGE / UPDATE                  │
#      │       │                             │
#      │       ▼                             │
#      │    Generator                        │
#      │                                     │
#      ▼                                     │
# Final Memory Operations                    │
#      │                                     │
#      ▼                                     │
# MemoryStore                                │
#      │                                     │
#      ▼                                     │
# PostgreSQL ◄───────────────────────────────┘

# -------------------------------------------------
# Extractor
# ↓
# Scorer
# ↓
# Evolution
# ↓
# Store
# Đây thực chất là một AI Processing Pipeline.
from app.services.ollama_service import OllamaService
from app.services.memory_store import MemoryStore
from app.schemas.memory_schema import Memory
from app.schemas.memory_decision_schema import MemoryDecision, MemoryAction
from app.prompts.memory_decision_prompt import build_memory_decision_prompt
from uuid import UUID


class MemoryEvolution:
    def __init__(self, ollama_service: OllamaService, memory_store: MemoryStore):
        self.ollama_service = ollama_service
        self.memory_store = memory_store

    def _search_candidates(self, user_id: UUID, memory: Memory) -> list[Memory]:

        print("\n\n Start search candidates \n\n", memory.content)
        memories = self.memory_store.search(
            user_id=user_id,
            query=memory.content,
            limit=5,
        )
        print("\n\n <--memories--> \n\n", memories)
        return memories

    def _decide(self, memory: Memory, candidates: list[Memory]):
        prompt = build_memory_decision_prompt(memory, candidates)
        messages = [
            {
                "role": "system",
                "content": prompt,
            }
        ]
        decision = self.ollama_service.generate_structured(
            messages=messages,
            response_model=MemoryDecision,
        )
        print("\n\n decision \n\n", decision)
        return decision

    def _execute(
        self,
        memory: Memory,
        candidates: list[Memory],
        decision: MemoryDecision,
    ) -> Memory | None:
        match decision.action:
            case MemoryAction.INSERT:
                return memory
            case MemoryAction.DUPLICATE:
                return None
            # case MemoryAction.MERGE:
            #     candidate = candidates[decision.candidate_index]

            # case MemoryAction.UPDATE:
            #     return memory  # TODO

        raise ValueError(f"Unsupported action: {decision.action}")

    def evolve(self, user_id: UUID, memories: list[Memory]) -> list[Memory]:
        final_memories: list[Memory] = []

        for memory in memories:
            candidates = self._search_candidates(user_id, memory)

            if not candidates:
                final_memories.append(memory)
                continue

            memory_decision = self._decide(memory, candidates)

            result = self._execute(
                memory,
                candidates,
                memory_decision,
            )

            if result:
                final_memories.append(result)

        return final_memories
