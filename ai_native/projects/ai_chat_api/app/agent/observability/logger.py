import logging

logger = logging.getLogger("agent")


def log_agent_event(
    event: str,
    *,
    run_id: str,
    trace_id: str | None = None,
    step: int | None = None,
    **fields,
) -> None:
    data = {
        "event": event,
        "run_id": run_id,
        "trace_id": trace_id,
    }

    if step is not None:
        data["step"] = step

    data.update(fields)

    logger.info(data)
