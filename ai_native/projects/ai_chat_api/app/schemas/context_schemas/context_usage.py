from pydantic import BaseModel


class ContextUsage(BaseModel):
    system_tokens: int
    memory_tokens: int
    rag_tokens: int
    history_tokens: int
    user_tokens: int

    @property
    def total_tokens(self) -> int:
        return (
            self.system_tokens
            + self.memory_tokens
            + self.rag_tokens
            + self.history_tokens
            + self.user_tokens
        )
