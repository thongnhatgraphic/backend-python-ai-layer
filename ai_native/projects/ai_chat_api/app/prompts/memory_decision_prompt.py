from app.schemas.memory_schema import Memory
import json


def build_memory_decision_prompt(memory: Memory, candidates: list[Memory]) -> str:
    return f"""
You are a memory evolution decision engine.
Your ONLY task is to decide what should happen to the new memory.

The new memory is: {json.dumps(
    memory.model_dump(),
    ensure_ascii=False,
    indent=2,
)}
The candidate memories are: {json.dumps(
    [m.model_dump() for m in candidates],
    ensure_ascii=False,
    indent=2,
)}

Possible actions:
INSERT
The new memory contains new information.
If no candidate is related,
choose INSERT.

DUPLICATE
The new memory has exactly the same meaning as one candidate.
Always compare semantic meaning, not wording.
Different wording with the same meaning 
should be considered DUPLICATE.

MERGE
The new memory complements one candidate.
If the new memory adds useful information to an existing memory,
prefer MERGE.

UPDATE
The new memory replaces outdated information.
If the new memory replaces outdated information,
prefer UPDATE.

Return ONLY JSON matching the schema.

"""
