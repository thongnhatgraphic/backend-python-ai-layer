import json
from collections.abc import Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.tests.agent.langgraph.lesson_18_streaming_agent import (
    agent_events,
)

app = FastAPI(title="LangGraph Streaming API")


class AgentStreamRequest(BaseModel):
    message: str


def stream_agent(message: str) -> Iterator[str]:
    inputs = {"messages": [HumanMessage(content=message)]}

    for event in agent_events(inputs):
        yield json.dumps(
            event,
            ensure_ascii=False,
        ) + "\n"
    yield json.dumps(
        {"type": "done"},
        ensure_ascii=False,
    ) + "\n"


@app.post("/agent/stream")
def agent_stream_endpoint(
    request: AgentStreamRequest,
) -> StreamingResponse:
    return StreamingResponse(
        stream_agent(request.message),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache"},
    )
