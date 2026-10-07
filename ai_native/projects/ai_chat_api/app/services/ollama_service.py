from typing import Literal, TypeVar, Callable
from ollama import Client
from pydantic import ValidationError

from app.core.settings import settings
import json

T = TypeVar("T")


class OllamaService:
    def __init__(self, client: Client = None):
        self.client = client
        self.model = settings.OLLAMA_MODEL
        self.options = {
            "num_ctx": settings.OLLAMA_NUM_CTX,
            "num_predict": settings.OLLAMA_NUM_PREDICT,
        }

    def generate(
        self,
        messages: list[dict[str, str]],
        format: Literal["text", "json"] = "text",
    ) -> str:

        kwargs = {
            "model": self.model,
            "messages": messages,
            "options": self.options,
        }

        if format == "json":
            kwargs["format"] = "json"

        response = self.client.chat(**kwargs)

        return response.message["content"]

    def generate_structured(
        self, messages: list[dict[str, str]], response_model: type[T]
    ) -> T:
        print("messages", messages)
        kwargs = {
            "model": self.model,
            "messages": messages,
            "options": self.options,
            "format": response_model.model_json_schema(),
        }

        response = self.client.chat(**kwargs)

        content = response.message["content"]
        print("content", content)
        try:
            data = json.loads(content)
            print("data", data)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON returned from LLM") from e

        try:
            return response_model.model_validate(data)
        except ValidationError as e:
            raise ValueError("Structured output validation failed") from e

    def chat_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict],
    ):
        response = self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            options=self.options,
        )

        return response
