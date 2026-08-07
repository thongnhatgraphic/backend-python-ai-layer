from openai import OpenAI
from app.core.settings import settings


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, prompt) -> str:
        response = self.client.responses.create(
            model=settings.DEFAULT_MODEL,
            input=prompt,
        )
        print("response", response)
        return response.output_text
