from app.services.ollama_service import OllamaService
from app.agent.tools.weather_tool import get_weather
import json

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get the weather for.",
                }
            },
            "required": ["city"],
        },
    },
}


class AgentRunner:
    def __init__(self, llm: OllamaService):
        self.llm = llm

    def run(self, user_message: str) -> str:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. " "Use the weather tool when needed."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        tools = [
            WEATHER_TOOL,
        ]
        print("\n\n tools \n\n")
        n = 1
        while True:
            print(f"Run {n} times")

            print("\n messages \n", messages)
            response = self.llm.chat_with_tools(
                messages=messages,
                tools=tools,
            )
            print("<--response-->", response.message)

            tool_calls = response.message.get(
                "tool_calls",
                [],
            )
            print("\n tool_calls \n", tool_calls)
            if not tool_calls:
                return response.message["content"]

            print(
                "\n response.message \n",
                response.message.get(
                    "content",
                    "",
                ),
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": response.message.get(
                        "content",
                        "",
                    ),
                    "tool_calls": tool_calls,
                }
            )
            print("\n If have tool calls \n", tool_calls)

            for tool_call in tool_calls:

                tool_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]

                if tool_name == "get_weather":
                    result = get_weather(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(result),
                    }
                )

            n += 1

        #        ┌──────────────┐
        #        │     User     │
        #        └──────┬───────┘
        #               ↓
        #        ┌──────────────┐
        #        │     LLM      │
        #        └──────┬───────┘
        #               ↓
        #          tool call?
        #         /          \
        #       no            yes
        #       ↓               ↓
        #   final answer      Backend
        #       ↓               ↓
        #      END             Tool
        #                       ↓
        #                  Tool result
        #                       ↓
        #                  messages[]
        #                       ↓
        #                      LLM


from ollama import Client
from app.core.settings import settings

client = Client(host=settings.OLLAMA_HOST)
# ollama_service = OllamaService(client)

agent_runner = AgentRunner(llm=OllamaService(client=client))

agent_runner.run("Thời tiết Huế hiện tại thế nào?")
