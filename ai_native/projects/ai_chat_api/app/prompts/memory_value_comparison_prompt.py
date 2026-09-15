from app.schemas.memory_schema import Memory
import json


def build_memory_value_comparison_prompt(
    new_memory: Memory,
    candidate: Memory,
) -> str:
    new_value = {
        "content": new_memory.content,
    }

    candidate_value = {
        "content": candidate.content,
    }
    return f"""
You are a memory value comparison engine.

Your ONLY task is to determine whether two memories represent
the same semantic value.

The application has already determined that both memories
belong to the same semantic slot.

NEW MEMORY:
{json.dumps(
    new_value,
    ensure_ascii=False,
    indent=2,
)}

EXISTING CANDIDATE:
{json.dumps(
    candidate_value,
    ensure_ascii=False,
    indent=2,
)}

Rules:
- Return same_value=true if both memories express the same fact/value.
- Different wording is still the same value.
- Return same_value=false if the value/state differs.
- Do not decide whether to INSERT, UPDATE, or MERGE.
- Only compare semantic value.

Return ONLY JSON matching the schema.
example:
{{
    
    "same_value": True,
    "reason": "Same semantic value ..."
    
}}
or 
{{
    
    "same_value": False,
    "reason": "..."
    
}}
"""
