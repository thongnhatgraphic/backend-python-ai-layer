from app.dependencies.ollama_dependency import get_ollama_service
from app.services.memory_evolution import MemoryEvolution
from app.services.memory_store import MemoryStore
from app.services.ollama_service import OllamaService
from app.dependencies.memory_store_dependency import get_memory_store
from fastapi import Depends


def get_memory_evolution(
    ollama: OllamaService = Depends(get_ollama_service),
    memory_store: MemoryStore = Depends(get_memory_store),
):
    return MemoryEvolution(ollama, memory_store)
