from app.dependencies.ollama_dependency import get_ollama_service
from app.services.memory_scorer import MemoryScorer


def get_memory_scorer():
    return MemoryScorer(get_ollama_service())
