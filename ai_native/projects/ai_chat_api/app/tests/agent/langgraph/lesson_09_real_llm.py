from typing_extensions import TypedDict, Annotated, Callable

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from langchain_ollama import ChatOllama

from app.core.settings import settings


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny and 30°C."


llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_HOST,
)

llm_with_tools = llm.bind_tools([get_weather])


response = llm_with_tools.invoke([HumanMessage(content="What is the weather in Hue?")])

print("CONTENT:", response.content)
print("TOOL CALLS:", response.tool_calls)
