from uuid import UUID
from app.schemas.memory_schema import Memory
from app.schemas.memory_search_schema import MemorySearchResult
from app.repositories.memory_repository import MemoryRepository
from uuid import uuid4


# MemoryStore chịu trách nhiệm truy xuất (retrieve) long-term memory phù hợp với một truy vấn.
class MemoryStore:
    def __init__(self, memory_repository: MemoryRepository):
        self.memory_repository = memory_repository

    def save(self, user_id: UUID, memories: list[Memory]):
        if not memories:
            return

        memories = [
            memory.model_copy(
                update={
                    "id": memory.id or uuid4(),
                }
            )
            for memory in memories
        ]

        self.memory_repository.save(
            user_id,
            memories,
        )

    def update(
        self,
        user_id: UUID,
        memories: list[Memory],
    ):
        if not memories:
            return

        self.memory_repository.update(
            user_id,
            memories,
        )

    def get_by_user_id(self, user_id: UUID) -> list[Memory]:
        return self.memory_repository.get(user_id)

    def search(
        self,
        user_id: UUID,
        query: str,
        limit: int = 5,
    ) -> list[Memory]:
        # Retrieval Ranking
        result = self.memory_repository.search(user_id, query, limit)

        return result

    def semantic_search(
        self, user_id: UUID, embedding: list[float], limit: int = 5
    ) -> list[MemorySearchResult]:
        return self.memory_repository.semantic_search(user_id, embedding, limit)
