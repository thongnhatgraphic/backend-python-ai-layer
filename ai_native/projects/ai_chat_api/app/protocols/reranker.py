from typing import Protocol
from app.schemas.retrieval_schema import RetrievalResult


class Reranker(Protocol):

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]: ...
