import asyncio
from typing_extensions import TypedDict, Annotated


from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy, TimeoutPolicy


class State(TypedDict):
    message: str


# Tool failure
# ├── immediate exception
# ├── timeout
# ├── validation error
# └── transient failure

attempts = 0


async def flaky_slow_node(state: State):
    global attempts
    attempts += 1

    print(f"slow_node attempt = {attempts}")

    if attempts < 3:
        await asyncio.sleep(2)
        return {"message": "This should timeout"}

    print("slow_node: finished")

    return {"message": "Done"}


builder = StateGraph(State)

builder.add_node(
    "flaky_slow_node",
    flaky_slow_node,
    timeout=TimeoutPolicy(run_timeout=1.0),
    retry_policy=RetryPolicy(
        max_attempts=3,
    ),
)

builder.add_edge(START, "flaky_slow_node")
builder.add_edge("flaky_slow_node", END)

graph = builder.compile()


if __name__ == "__main__":
    asyncio.run(graph.ainvoke({"message": "Hello"}))
