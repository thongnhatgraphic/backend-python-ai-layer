from uuid import UUID
from app.schemas.memory_schema import Memory
from app.repositories.memory_repository import MemoryRepository


# MemoryStore chịu trách nhiệm truy xuất (retrieve) long-term memory phù hợp với một truy vấn.
class MemoryStore:
    def __init__(self, memory_repository: MemoryRepository):
        self.memory_repository = memory_repository

    def save(self, user_id: UUID, memories: list[Memory]):
        if not memories:
            return

        unique_contents = set()
        filtered_memories = []
        for memory in memories:

            if memory.content in unique_contents:
                continue

            unique_contents.add(memory.content)
            filtered_memories.append(memory)

        print("filtered_memories", filtered_memories)

        self.memory_repository.save(
            user_id,
            filtered_memories,
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
