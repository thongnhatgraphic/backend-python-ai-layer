#               ToolExecutor
#                    │
#                    ↓
#             IdempotencyService
#                    │
#          ┌─────────┴─────────┐
#          ↓                   ↓
#       reserve              get
#          │                   │
#          ↓                   ↓
#     acquired?              state?
#       /      \            /       \
#     YES       NO         /         \
#      ↓         ↓         ↓           ↓
#   execute    inspect  PROCESSING  COMPLETED
#      ↓         │         ↓           ↓
#   complete     └─────→  poll      result
#      ↓                   ↓
#  COMPLETED           COMPLETED

# Retry backoff
# → dùng khi EXECUTE LẠI

# Polling interval
# → dùng khi CHỜ operation đang chạy


#           Tool Execution
#                 │
#     ┌───────────┼───────────┐
#     ↓           ↓           ↓
#  Timeout      Retry     Idempotency
#                             │
#                             ↓
#                           Lease
#                             │
#                      ┌──────┴──────┐
#                      ↓             ↓
#                   renew         ownership

import logging
import time
import asyncio

from pydantic import ValidationError
from app.agent.errors.tool_errors import ToolError, ToolValidationError

from app.agent.definitions.tool_definition import ToolDefinition

from app.agent.policies.retry_policy import RetryPolicy
from app.agent.observability.context import AgentExecutionContext
from app.agent.observability.metrics import AgentMetrics
from app.agent.observability.tracing import tracer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


class ToolExecutor:
    def __init__(self, retry_policy: RetryPolicy, metrics: AgentMetrics):
        self.retry_policy = retry_policy
        self.metrics = metrics

    def execute(
        self, tool: ToolDefinition, arguments: dict, *, context: AgentExecutionContext
    ) -> dict:

        logger.info(
            "Tool execution started: tool=%s | run_id=%s | trace_id=%s | step=%s",
            tool.name,
            context.run_id,
            context.trace_id,
            context.step,
        )

        # 1. Validate ONCE
        try:

            validated_input = tool.input_model.model_validate(arguments)
            print("validated input success", validated_input)

        except ValidationError as exc:
            logger.warning(
                "Tool validation failed: tool=%s",
                tool.name,
            )

            raise ToolValidationError(
                f"Invalid arguments for tool '{tool.name}'"
            ) from exc

        self.metrics.increment_tool_calls(tool.name)
        # 2. Retry only execution
        attempt = 1
        with tracer.start_as_current_span(f"tool.{tool.name}") as span:
            span.set_attribute("agent.run_id", context.run_id)
            span.set_attribute("agent.step", context.step)
            span.set_attribute("tool.name", tool.name)

            while True:
                try:
                    started_at = time.perf_counter()

                    result = tool.function(**validated_input.model_dump())

                    latency_ms = (time.perf_counter() - started_at) * 1000

                    self.metrics.observe_tool_latency(
                        tool.name,
                        latency_ms / 1000,
                    )

                    logger.info(
                        "Tool execution completed: tool=%s run_id=%s trace_id=%s step=%s attempt=%s latency_ms=%.2f",
                        tool.name,
                        context.run_id,
                        context.trace_id,
                        context.step,
                        attempt,
                        latency_ms,
                    )

                    return result

                except ToolError as exc:
                    if not self.retry_policy.should_retry(
                        exc,
                        attempt,
                    ):
                        logger.warning(
                            "Tool execution failed: tool=%s | attempt=%s | error=%s",
                            tool.name,
                            attempt,
                            type(exc).__name__,
                        )
                        raise

                    span.add_event(
                        "tool.retry",
                        {
                            "tool.name": tool.name,
                            "attempt": attempt,
                            "error.type": type(exc).__name__,
                        },
                    )

                    delay = self.retry_policy.get_delay(attempt)

                    logger.warning(
                        "Retrying tool: tool=%s | attempt=%s | delay=%.3fs | error=%s",
                        tool.name,
                        attempt,
                        delay,
                        type(exc).__name__,
                    )

                    time.sleep(delay)
                    # await asyncio.sleep(delay)

                    attempt += 1


# logger.info(
#     "Tool execution completed: tool=%s",
#     tool.name,
# )

# return result
