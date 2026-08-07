from app.services.openai_service import OpenAIService

service = OpenAIService()

response = service.generate("Explain Redis in one paragraph.")

print(response)
