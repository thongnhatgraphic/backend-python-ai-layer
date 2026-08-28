from app.dependencies.ollama_dependency import client
from app.services.embedding_service import EmbeddingService

embedding_service = EmbeddingService(client)


def get_embedding_dependency() -> EmbeddingService:
    return embedding_service
