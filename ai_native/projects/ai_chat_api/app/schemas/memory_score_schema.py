from pydantic import BaseModel, Field


class MemoryScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0)


class MemoryScoreList(BaseModel):
    memories: list[MemoryScore]
