from app.agent.errors.tool_errors import ToolTransientError, ToolExecutionError

_attempts = 0


def flaky_tool(arg1: str) -> dict:
    global _attempts

    _attempts += 1

    print("Just Print", arg1)

    if _attempts < 3:
        raise ToolTransientError(f"Temporary failure on attempt {_attempts}")
        # raise ToolExecutionError(f"Tool execution failed on attempt {_attempts}")

    return {
        "status": "success",
        "attempt": _attempts,
    }
