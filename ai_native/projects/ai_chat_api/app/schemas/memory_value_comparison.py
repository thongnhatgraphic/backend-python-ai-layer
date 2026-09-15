from pydantic import BaseModel, Field


class MemoryValueComparison(BaseModel):
    same_value: bool
    reason: str
