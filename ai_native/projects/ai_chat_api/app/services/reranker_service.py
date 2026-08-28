import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.schemas.memory_search_schema import MemorySearchResult
from app.schemas.memory_rerank_schema import MemoryRerankResult
from app.schemas.memory_schema import Memory


class RerankerService:
    def __init__(
        self,
        tokenizer: AutoTokenizer,
        model: AutoModelForSequenceClassification,
    ):
        self.tokenizer = tokenizer
        self.model = model

    def rerank(
        self,
        query: str,
        memories: list[MemorySearchResult],
        limit: int = 5,
    ) -> list[MemoryRerankResult]:
        if not memories:
            return []

        queries = [query for _ in memories]

        documents = [memory.memory.content for memory in memories]

        inputs = self.tokenizer(
            queries,
            text_pair=documents,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512,
        )

        with torch.no_grad():
            scores = (
                self.model(**inputs, return_dict=True).logits.view(-1).float().tolist()
            )

        memories_reranked: list[MemoryRerankResult] = [
            MemoryRerankResult(
                score=score,
                memory=Memory(
                    id=memory.memory.id,
                    content=memory.memory.content,
                    # embedding=memory.memory.embedding,
                    category=memory.memory.category,
                    memory_key=memory.memory.memory_key,
                    cardinality=memory.memory.cardinality,
                    temporal_behavior=memory.memory.temporal_behavior,
                ),
            )
            for memory, score in zip(
                memories,
                scores,
            )
        ]

        memories_reranked.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        return memories_reranked[:limit]
