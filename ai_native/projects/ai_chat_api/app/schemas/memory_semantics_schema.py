from enum import Enum
from pydantic import BaseModel, Field


class Cardinality(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class TemporalBehavior(str, Enum):
    CURRENT = "current"
    HISTORICAL = "historical"
    EVENT = "event"


class MemorySemantics(BaseModel):
    category: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z][a-z0-9_]*$",
    )
    memory_key: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z][a-z0-9_]*$",
    )
    cardinality: Cardinality
    temporal_behavior: TemporalBehavior
