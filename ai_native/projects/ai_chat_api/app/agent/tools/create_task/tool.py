from app.agent.errors.tool_errors import ToolTimeoutError

_create_count = 0


def create_task(title: str) -> dict:
    global _create_count

    _create_count += 1

    print(f"Creating task. count={_create_count}")

    if _create_count > 3:
        # Giả lập:
        # DB đã commit nhưng response bị timeout
        raise ToolTimeoutError("Response timed out after task was created")

    return {
        "task_id": f"task-{_create_count}",
        "title": title,
    }
