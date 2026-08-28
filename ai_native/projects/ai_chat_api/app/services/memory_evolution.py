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

# ------------------------------------------------

# 1     INSERT=====================================
# Không có memory tương ứng
# → thêm memory
# 2     DUPLICATE=====================================
# Cùng semantic fact
# → không làm gì
# 3     UPDATE=====================================
# Cùng slot
# +
# single-value
# +
# giá trị mới thay thế giá trị cũ
# → update existing row
# 4     MERGE=====================================
# Hai facts liên quan
# +
# cả hai vẫn đúng
# +
# có thể tạo một representation tốt hơn
# → merge

# Đây là domain meaning, không phải chỉ là enum.

#                  MemoryEvolution
#                         │
#                  semantic matching
#                         │
#              ┌──────────┴──────────┐
#              │                     │
#         Same semantic slot?     No match
#              │                     │
#             YES                   LLM
#              │                     │
#       deterministic policy    INSERT / MERGE
#              │
#        ┌─────┴─────┐
#        ↓           ↓
#     same value  new value
#        ↓           ↓
#    DUPLICATE    UPDATE

from app.services.ollama_service import OllamaService
from app.services.memory_store import MemoryStore
from app.schemas.memory_schema import Memory
from app.schemas.memory_decision_schema import MemoryDecision, MemoryAction
from app.schemas.memory_evolution_schema import (
    MemoryEvolutionResult,
    MemoryEvolutionOperation,
)
from app.schemas.memory_value_comparison import MemoryValueComparison
from app.schemas.memory_semantics_schema import Cardinality, TemporalBehavior
from app.prompts.memory_decision_prompt import build_memory_decision_prompt
from app.prompts.memory_value_comparison_prompt import (
    build_memory_value_comparison_prompt,
)
from uuid import UUID


class MemoryEvolution:
    def __init__(self, ollama_service: OllamaService, memory_store: MemoryStore):
        self.ollama_service = ollama_service
        self.memory_store = memory_store

    def _validate_decision(
        self,
        decision: MemoryDecision,
        candidates: list[Memory],
    ) -> None:
        action = decision.action
        candidate_index = decision.candidate_index
        resulting_content = decision.resulting_content

        # INSERT
        if action == MemoryAction.INSERT:
            if candidate_index is not None:
                raise ValueError("INSERT decision must not contain candidate_index")

            if resulting_content is not None:
                raise ValueError("INSERT decision must not contain resulting_content")

            return

        # DUPLICATE / UPDATE / MERGE
        if candidate_index is None:
            raise ValueError(
                f"{action.value.upper()} decision requires candidate_index"
            )

        if not 0 <= candidate_index < len(candidates):
            raise ValueError(
                f"candidate_index={candidate_index} "
                f"is out of range. "
                f"Candidates count={len(candidates)}"
            )

        # DUPLICATE
        if action == MemoryAction.DUPLICATE:
            if resulting_content is not None:
                raise ValueError(
                    "DUPLICATE decision must not contain resulting_content"
                )

            return

        # UPDATE / MERGE
        if action in (
            MemoryAction.UPDATE,
            MemoryAction.MERGE,
        ):
            if not resulting_content:
                raise ValueError(
                    f"{action.value.upper()} decision " "requires resulting_content"
                )

            return

        raise ValueError(f"Unsupported memory action: {action}")

    def _search_candidates(self, user_id: UUID, memory: Memory) -> list[Memory]:

        print("\n\n Start search candidates \n\n", memory.content)
        results = self.memory_store.semantic_search(
            user_id=user_id,
            embedding=memory.embedding,
            limit=5,
        )
        print("\n\n <--memories--> \n\n", results)
        return [result.memory for result in results]

    def _decide(
        self,
        memory: Memory,
        candidates: list[Memory],
        *,
        allowed_actions: set[MemoryAction] | None = None,
    ) -> MemoryDecision:
        prompt = build_memory_decision_prompt(
            memory, candidates, allowed_actions=allowed_actions
        )
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
    ) -> MemoryEvolutionResult | None:
        match decision.action:
            case MemoryAction.INSERT:
                return MemoryEvolutionResult(
                    operation=MemoryEvolutionOperation.INSERT, memory=memory
                )
            case MemoryAction.DUPLICATE:
                return MemoryEvolutionResult(
                    operation=MemoryEvolutionOperation.DUPLICATE,
                    memory=None,
                )
            case MemoryAction.UPDATE:
                if decision.candidate_index is None:
                    raise ValueError("UPDATE requires candidate_index")

                candidate = candidates[decision.candidate_index]

                if decision.resulting_content is None:
                    raise ValueError("UPDATE requires resulting_content")

                return MemoryEvolutionResult(
                    operation=MemoryEvolutionOperation.UPDATE,
                    memory=Memory(
                        id=candidate.id,
                        content=decision.resulting_content,
                        category=candidate.category,
                        memory_key=candidate.memory_key,
                        cardinality=candidate.cardinality,
                        temporal_behavior=candidate.temporal_behavior,
                        embedding=None,
                    ),
                )

            case MemoryAction.MERGE:
                if decision.candidate_index is None:
                    raise ValueError("MERGE requires candidate_index")

                if decision.resulting_content is None:
                    raise ValueError("MERGE requires resulting_content")

                candidate = candidates[decision.candidate_index]

                return MemoryEvolutionResult(
                    operation=MemoryEvolutionOperation.UPDATE,
                    memory=Memory(
                        id=candidate.id,
                        content=decision.resulting_content,
                        category=candidate.category,
                        memory_key=candidate.memory_key,
                        cardinality=candidate.cardinality,
                        temporal_behavior=candidate.temporal_behavior,
                        embedding=None,
                    ),
                )

        raise ValueError(f"Unsupported action: {decision.action}")

    def _find_semantic_slot_match(
        self,
        memory: Memory,
        candidates: list[Memory],
    ) -> Memory | None:
        for candidate in candidates:
            if (
                memory.category == candidate.category
                and memory.memory_key == candidate.memory_key
                and memory.cardinality == candidate.cardinality
                and memory.temporal_behavior == candidate.temporal_behavior
            ):
                return candidate

        return None

    def _should_update(
        self,
        memory: Memory,
        candidate: Memory,
    ) -> bool:
        return (
            memory.cardinality == Cardinality.SINGLE
            and candidate.cardinality == Cardinality.SINGLE
            and memory.temporal_behavior == TemporalBehavior.CURRENT
            and candidate.temporal_behavior == TemporalBehavior.CURRENT
        )

    def _build_state_decision(
        self,
        memory: Memory,
        candidate: Memory,
        candidate_index: int,
    ) -> MemoryDecision:
        comparison = self._compare_memory_values(
            memory,
            candidate,
        )
        print("\n\n comparison \n\n", comparison)

        if comparison.same_value:
            return MemoryDecision(
                action=MemoryAction.DUPLICATE,
                candidate_index=candidate_index,
                resulting_content=None,
                reason=comparison.reason,
            )

        return MemoryDecision(
            action=MemoryAction.UPDATE,
            candidate_index=candidate_index,
            resulting_content=memory.content,
            reason=comparison.reason,
        )

    def _compare_memory_values(
        self,
        memory: Memory,
        candidate: Memory,
    ) -> MemoryValueComparison:
        prompt = build_memory_value_comparison_prompt(
            memory,
            candidate,
        )
        messages = [
            {
                "role": "system",
                "content": prompt,
            }
        ]

        result = self.ollama_service.generate_structured(
            messages=messages,
            response_model=MemoryValueComparison,
        )

        return result

    def evolve(
        self, user_id: UUID, memories: list[Memory]
    ) -> list[MemoryEvolutionResult]:
        results: list[MemoryEvolutionResult] = []

        for memory in memories:
            if memory.embedding is None:
                raise ValueError(
                    "Memory embedding is required " "before MemoryEvolution"
                )

            candidates = self._search_candidates(user_id, memory)

            if not candidates:
                results.append(
                    MemoryEvolutionResult(
                        operation=MemoryEvolutionOperation.INSERT, memory=memory
                    )
                )
                continue

            semantic_match = self._find_semantic_slot_match(
                memory,
                candidates,
            )

            if semantic_match and self._should_update(
                memory,
                semantic_match,
            ):
                candidate_index = candidates.index(semantic_match)

                decision = self._build_state_decision(
                    memory,
                    semantic_match,
                    candidate_index,
                )
            else:
                decision = self._decide(
                    memory,
                    candidates,
                    allowed_actions=None,
                )

            self._validate_decision(
                decision,
                candidates,
            )

            result = self._execute(
                memory,
                candidates,
                decision,
            )

            if result:
                results.append(result)

        return results
