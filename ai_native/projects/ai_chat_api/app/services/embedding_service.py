from ollama import Client
from app.core.settings import settings
from app.schemas.memory_schema import Memory


class EmbeddingService:
    def __init__(self, client: Client | None):
        self.client = client
        self.model = settings.OLLAMA_EMBEDDING_MODEL

    def embed(
        self,
        text: str,
    ) -> list[float]:
        result = self.client.embed(model=self.model, input=text)

        return result.embeddings[0]

    def batch_embed(
        self,
        memories: list[Memory],
    ) -> list[list[float]]:
        result = self.client.embed(
            model=self.model,
            input=[memory.content for memory in memories],
        )

        return result.embeddings
