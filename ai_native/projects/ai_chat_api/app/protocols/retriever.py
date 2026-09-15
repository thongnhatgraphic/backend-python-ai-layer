from typing import Protocol
from app.schemas.retrieval_schema import RetrievalResult

# Pydantic BaseModel = DATA CONTRACT
# Protocol           = BEHAVIOR CONTRACT


class Retriever(Protocol):

    def search(self, query: str, limit: int = 10) -> list[RetrievalResult]: ...
