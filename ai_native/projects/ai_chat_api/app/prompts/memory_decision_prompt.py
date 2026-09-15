from app.schemas.memory_schema import Memory
from app.schemas.memory_decision_schema import MemoryAction
import json


def build_memory_decision_prompt(
    memory: Memory, candidates: list[Memory], allowed_actions
) -> str:
    new_memory = {
        "content": memory.content,
        "semantics": {
            "category": memory.category,
            "memory_key": memory.memory_key,
            "cardinality": memory.cardinality,
            "temporal_behavior": memory.temporal_behavior,
        },
    }

    candidate_memories = [
        {
            "candidate_index": index,
            "content": candidate.content,
            "semantics": {
                "category": candidate.category,
                "memory_key": candidate.memory_key,
                "cardinality": candidate.cardinality,
                "temporal_behavior": candidate.temporal_behavior,
            },
        }
        for index, candidate in enumerate(candidates)
    ]
    if allowed_actions is None:
        allowed_actions = set(MemoryAction)

    allowed_action_names = {action.value.upper() for action in allowed_actions}

    same_slot_rule = ""
    if (
        MemoryAction.DUPLICATE in allowed_actions
        or MemoryAction.UPDATE in allowed_actions
        or MemoryAction.MERGE in allowed_actions
    ) and MemoryAction.INSERT not in allowed_actions:
        same_slot_rule = """
            The application has already determined that the new memory
            and at least one candidate belong to the same semantic slot.

            Therefore:
            - INSERT is NOT allowed.
            - You MUST choose one of the allowed actions.
        """

    return f"""
You are a memory evolution decision engine.

Your ONLY task is to decide what should happen to the new memory.

The application has already performed deterministic semantic analysis.
You MUST respect that analysis.

NEW MEMORY:
{json.dumps(
    new_memory,
    ensure_ascii=False,
    indent=2,
)}

CANDIDATE MEMORIES:
{json.dumps(
    candidate_memories,
    ensure_ascii=False,
    indent=2,
)}

ALLOWED ACTIONS:
{json.dumps(
    sorted(allowed_action_names),
    ensure_ascii=False,
)}

{same_slot_rule}

ACTION DEFINITIONS:

DUPLICATE
- The new memory expresses the same semantic fact as a candidate.
- Different wording with the same meaning is still DUPLICATE.
- candidate_index must identify the matching candidate.
- resulting_content must be null.

UPDATE
- The new memory represents a newer value/state
  that supersedes a candidate.
- The candidate represents outdated information.
- candidate_index must identify the outdated candidate.
- resulting_content must contain the final memory content
  that should replace the candidate.

MERGE
- Both the new memory and candidate remain true.
- The new memory adds useful information.
- Combine them into one concise memory.
- candidate_index must identify the candidate to merge with.
- resulting_content must contain the final merged content.

INSERT
- The new memory represents genuinely new information
  that does not correspond to an existing candidate.
- candidate_index must be null.
- resulting_content must be null.

IMPORTANT RULES:

1. Choose exactly ONE action.
2. You may ONLY choose an action from ALLOWED ACTIONS.
3. candidate_index must be provided for DUPLICATE, UPDATE, or MERGE.
4. candidate_index must be null for INSERT.
5. resulting_content is required for UPDATE and MERGE.
6. resulting_content must be null for INSERT and DUPLICATE.
7. Never modify or invent semantic metadata.
8. Use only information supported by the new memory and candidates.
9. Do not create additional memories.
10. Return ONLY valid JSON matching the schema.

"""
