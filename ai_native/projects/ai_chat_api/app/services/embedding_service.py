from ollama import Client
from app.core.settings import settings


class EmbeddingService:
    def __init__(self, client: Client):
        self.client = client
        self.model = settings.OLLAMA_EMBEDDING_MODEL

    def embed(
        self,
        text: str,
    ) -> list[float]:
        result = self.client.embed(model=self.model, input=text)
        print("type(vector)", type(result))
        print(len(result.embeddings[0]))
        print(result.embeddings[0][:10])

        return result.embeddings[0]

    def batch_embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        result = self.client.embed(
            model=self.model,
            input=texts,
        )
        for i in result.embeddings:
            print("type(vector)", type(i))
            print(len(i))

        return result.embeddings
