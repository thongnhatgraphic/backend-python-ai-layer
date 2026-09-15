from app.services.memory_extractor import MemoryExtractor
from app.dependencies.ollama_dependency import ollama_service


def get_memory_extractor() -> MemoryExtractor:
    return MemoryExtractor(ollama_service)
