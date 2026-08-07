from pydantic import BaseModel


class MemoryScore(BaseModel):
    content: str
    score: float


class MemoryScoreList(BaseModel):
    memories: list[MemoryScore]
