from ollama import Client

from app.core.settings import settings
from app.services.ollama_service import OllamaService

client = Client(host=settings.OLLAMA_HOST)
ollama_service = OllamaService(client)


def get_ollama_service() -> OllamaService:
    return ollama_service
