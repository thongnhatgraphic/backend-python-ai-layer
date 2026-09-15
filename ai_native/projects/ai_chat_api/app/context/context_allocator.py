# Global Context Budget
#          │
#          ▼
# ┌─────────────────┐
# │ ContextCandidate│
# └─────────────────┘
#    │      │      │
#    ▼      ▼      ▼
# Memory   RAG   History
#    │      │      │
# demand  demand demand
#    │      │      │
#  max    max     max
#    │      │      │
#    └──────┼──────┘
#           ▼
#  ContextAllocator
#           │
#  Priority tiers
#           │
#           ▼
# ContextAllocation
from collections import defaultdict

from app.schemas.context_schemas.context_candidate import ContextCandidate
from app.schemas.context_schemas.context_allocation import ContextAllocation
from app.context.context_priority import ContextImportance

PRIORITY_ORDER = [
    ContextImportance.HIGH,
    ContextImportance.MEDIUM,
    ContextImportance.LOW,
]


class ContextAllocator:
    def __init__(self):
        pass

    def allocate(
        self,
        budget: int,
        candidates: list[ContextCandidate],
    ) -> ContextAllocation:

        if budget <= 0:
            return ContextAllocation()

        allocations = defaultdict(int)

        # ---------------------------------------------------------
        # Step 1:
        # Calculate effective demand.
        #
        # We never allow a candidate to request more than its
        # configured maximum useful capacity.
        # ---------------------------------------------------------
        effective_candidates: list[ContextCandidate] = []

        for candidate in candidates:

            if candidate.priority == ContextImportance.NONE:
                continue

            if candidate.demand_tokens <= 0:
                continue

            effective_demand = min(
                candidate.demand_tokens,
                candidate.max_tokens,
            )

            if effective_demand <= 0:
                continue

            effective_candidates.append(
                candidate.model_copy(
                    update={
                        "demand_tokens": effective_demand,
                    }
                )
            )

        remaining_budget = budget

        # ---------------------------------------------------------
        # Step 2:
        # Process priority tiers.
        #
        # HIGH → MEDIUM → LOW
        # ---------------------------------------------------------
        for priority in PRIORITY_ORDER:

            if remaining_budget <= 0:
                break

            tier_candidates = [
                candidate
                for candidate in effective_candidates
                if candidate.priority == priority
            ]

            if not tier_candidates:
                continue

            tier_demand = sum(candidate.demand_tokens for candidate in tier_candidates)

            # -----------------------------------------------------
            # Case A:
            # The entire tier can be satisfied.
            # -----------------------------------------------------
            if tier_demand <= remaining_budget:

                for candidate in tier_candidates:
                    allocations[candidate.name] = candidate.demand_tokens

                remaining_budget -= tier_demand
                continue

            # -----------------------------------------------------
            # Case B:
            # The tier cannot be fully satisfied.
            #
            # Distribute the entire remaining budget proportionally
            # according to demand.
            # -----------------------------------------------------
            raw_allocations: dict[str, float] = {}

            for candidate in tier_candidates:

                raw_allocations[candidate.name] = (
                    remaining_budget * candidate.demand_tokens / tier_demand
                )

            # Integer allocation first.
            allocated_now = 0

            for name, raw_value in raw_allocations.items():

                amount = int(raw_value)

                allocations[name] += amount
                allocated_now += amount

            # -----------------------------------------------------
            # Step 3:
            # Handle rounding remainder.
            # Largest fractional remainder gets the extra token.
            #
            # Name is used as deterministic tie-breaker.
            # -----------------------------------------------------
            remaining_tokens = remaining_budget - allocated_now

            if remaining_tokens > 0:

                ordered = sorted(
                    raw_allocations.items(),
                    key=lambda item: (
                        -(item[1] - int(item[1])),
                        item[0],
                    ),
                )

                for name, _ in ordered:

                    if remaining_tokens <= 0:
                        break

                    allocations[name] += 1
                    remaining_tokens -= 1

            remaining_budget = 0

        return ContextAllocation(
            memory_tokens=allocations.get("memory", 0),
            rag_tokens=allocations.get("rag", 0),
            history_tokens=allocations.get("history", 0),
        )
