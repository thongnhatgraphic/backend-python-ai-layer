from pydantic import BaseModel


class ContextAllocation(BaseModel):
    memory_tokens: int = 0
    rag_tokens: int = 0
    history_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.memory_tokens + self.rag_tokens + self.history_tokens
