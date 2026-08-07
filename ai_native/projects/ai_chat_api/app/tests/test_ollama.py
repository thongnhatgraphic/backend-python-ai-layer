from app.services.ollama_service import OllamaService

service = OllamaService()

response = service.chat("Explain Redis in one paragraph.")

print(response)
