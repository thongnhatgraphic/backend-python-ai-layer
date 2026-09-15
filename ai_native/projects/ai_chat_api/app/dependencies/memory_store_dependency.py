from app.database import get_session
from app.services.memory_store import MemoryStore
from fastapi import Depends
from app.repositories.memory_repository import MemoryRepository


def get_memory_store(session=Depends(get_session)) -> MemoryStore:
    repository = MemoryRepository(session)

    return MemoryStore(repository)
