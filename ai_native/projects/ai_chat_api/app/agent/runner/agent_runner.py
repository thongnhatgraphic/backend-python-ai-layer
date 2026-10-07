import json
from uuid import uuid4
import time


from app.services.ollama_service import OllamaService

from app.agent.tools.registry import ToolRegistry
from app.agent.state_store.store import AgentStateStore
from app.agent.state_store.redis_store import RedisAgentStateStore
from app.agent.confirmation.models import ConfirmationRequest
from app.agent.policies.tool_policy import ToolPolicy, ToolPolicyDecision
from app.agent.executors.tool_executor import ToolExecutor
from app.agent.errors.tool_errors import (
    ToolError,
    ToolPolicyError,
)
from app.agent.state import AgentState, AgentStatus, ResponseType, PendingConfirmation

from app.agent.observability.logger import log_agent_event
from app.agent.observability.context import AgentExecutionContext
from app.agent.observability.metrics import AgentMetrics
from app.agent.observability.tracing import tracer

# ToolPolicy
#     → "Được phép chạy không?"

# RetryPolicy
#     → "Nếu chạy lỗi transient thì retry thế nào?"


# ToolExecutor
#     → "Thực thi tool"
class AgentRunner:
    def __init__(
        self,
        llm: OllamaService,
        tool_registry: ToolRegistry,
        tool_executor: ToolExecutor,
        tool_policy: ToolPolicy,
        state_store: RedisAgentStateStore,
        metrics: AgentMetrics,
    ):
        self.llm = llm
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor
        self.tool_policy = tool_policy
        self.state_store = state_store
        self.metrics = metrics

    @staticmethod
    def _classify_response(response) -> ResponseType:
        content = response.message.get("content", "")
        tool_calls = response.message.get("tool_calls", [])

        if tool_calls:
            return ResponseType.TOOL_CALL

        if content.strip():
            return ResponseType.FINAL

        return ResponseType.NO_PROGRESS

    def _handle_response(
        self,
        state: AgentState,
        response,
    ) -> AgentStatus:
        response_type = self._classify_response(response)

        content = response.message.get("content", "")
        tool_calls = response.message.get(
            "tool_calls",
            [],
        )

        match response_type:
            case ResponseType.TOOL_CALL:
                state.status = AgentStatus.RUNNING
                state.messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                        "tool_calls": tool_calls,
                    }
                )
                state.no_progress_retries = 0
                for tool_call in tool_calls:
                    tool_call_id = str(uuid4())

                    try:
                        tool_name = tool_call["function"]["name"]
                        arguments = tool_call["function"]["arguments"]

                        definition = self.tool_registry.get(tool_name)

                        policy_result = self.tool_policy.check(definition)

                        log_agent_event(
                            "tool.policy_decision",
                            run_id=state.run_id,
                            trace_id=state.trace_id,
                            step=state.step,
                            tool_name=tool_name,
                            decision=policy_result.decision.value,
                        )

                        match policy_result.decision:

                            case ToolPolicyDecision.ALLOW:
                                result = self.tool_executor.execute(
                                    definition,
                                    arguments,
                                    context=AgentExecutionContext(
                                        run_id=state.run_id,
                                        trace_id=state.trace_id,
                                        step=state.step,
                                    ),
                                )

                                state.messages.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call_id,
                                        "content": json.dumps(result),
                                    }
                                )

                            case ToolPolicyDecision.REQUIRE_CONFIRMATION:

                                state.pending_confirmation = PendingConfirmation(
                                    tool_call_id=tool_call_id,
                                    tool_name=tool_name,
                                    arguments=arguments,
                                    reason=policy_result.reason,
                                )

                                self._set_status(
                                    state,
                                    AgentStatus.WAITING_FOR_CONFIRMATION,
                                )

                                log_agent_event(
                                    "agent.waiting_for_confirmation",
                                    run_id=state.run_id,
                                    trace_id=state.trace_id,
                                    step=state.step,
                                    tool_call_id=tool_call_id,
                                    tool_name=tool_name,
                                )
                                break

                            case ToolPolicyDecision.REJECT:
                                state.status = AgentStatus.FAILED
                                raise ToolPolicyError(policy_result.reason)

                    except ToolError:
                        self._set_status(state, AgentStatus.FAILED)
                        raise

            case ResponseType.FINAL:
                state.messages.append(
                    {
                        "role": "assistant",
                        "content": response.message["content"],
                    }
                )
                self._set_status(state, AgentStatus.COMPLETED)
                print("FINAL STATE")
                print("AgentState Finished Step =>>>>", state.step)
                print("AgentState messages =>>>>", state.messages)

            case ResponseType.NO_PROGRESS:
                state.no_progress_retries += 1

                print(
                    "NO_PROGRESS attempt #",
                    state.no_progress_retries,
                )

                if state.no_progress_retries > state.max_no_progress_retries:
                    state.status = AgentStatus.FAILED
                    print("Agent failed because of repeated NO_PROGRESS")
                    raise RuntimeError("Agent produced no progress")

                state.status = AgentStatus.RUNNING

        # print("status", state.status)
        return state.status

    def _run_loop(self, state: AgentState) -> AgentState:

        tools = self.tool_registry.get_all()

        while True:

            if state.step >= state.max_steps:
                # state.status = AgentStatus.STEP_LIMIT_EXCEEDED
                self._set_status(state, AgentStatus.STEP_LIMIT_EXCEEDED)

                state.messages.append(
                    {
                        "role": "assistant",
                        "content": "The agent has reached the maximum number of steps.",
                    }
                )

                self.state_store.save(state)
                break

            state.step += 1

            log_agent_event(
                f"llm.started #{state.step}",
                run_id=state.run_id,
                trace_id=state.trace_id,
                step=state.step,
            )

            started_at = time.perf_counter()

            try:
                self.metrics.increment_llm_calls()

                with tracer.start_as_current_span("llm.call") as span:
                    span.set_attribute("agent.run_id", state.run_id)
                    span.set_attribute("agent.step", state.step)

                    try:
                        response = self.llm.chat_with_tools(
                            messages=state.messages,
                            tools=[tool.to_llm_schema() for tool in tools],
                        )
                    except Exception:
                        raise
            finally:
                latency_ms = (time.perf_counter() - started_at) * 1000
                self.metrics.observe_llm_latency(latency_ms / 1000)

            log_agent_event(
                "llm.completed",
                run_id=state.run_id,
                trace_id=state.trace_id,
                step=state.step,
                latency_ms=round(latency_ms, 4),
            )

            status = self._handle_response(
                state,
                response,
            )

            # Persist the latest state snapshot
            self.state_store.save(state)

            if status in {
                AgentStatus.COMPLETED,
                AgentStatus.WAITING_FOR_CONFIRMATION,
                AgentStatus.CANCELLED,
                AgentStatus.FAILED,
                AgentStatus.STEP_LIMIT_EXCEEDED,
            }:
                break

        return state

    def run(self, user_message: str) -> AgentState:
        messages = [
            {"role": "system", "content": "You are a helpful assistant. "},
            {
                "role": "user",
                "content": user_message,
            },
        ]
        state = AgentState(user_message=user_message, messages=messages, max_steps=3)
        self.metrics.increment_agent_runs()

        with tracer.start_as_current_span("agent.run") as span:
            span.set_attribute("agent.run_id", state.run_id)
            span.set_attribute("agent.user_message", user_message)

            return self._run_loop(state)

    def confirm(
        self,
        run_id: str,
        request: ConfirmationRequest,
    ) -> AgentState:

        state: AgentState = self.state_store.get(run_id)

        if state is None:
            raise RuntimeError("Agent run not found.")

        if state.status != AgentStatus.WAITING_FOR_CONFIRMATION:
            raise RuntimeError("Agent is not waiting for confirmation")

        pending = state.pending_confirmation
        print("\n pending \n", pending)

        if pending is None:
            raise RuntimeError("No pending confirmation found.")

        if pending.tool_call_id != request.tool_call_id:
            raise RuntimeError("Tool call ID does not match pending confirmation.")

        # User declined
        if not request.approved:
            state.pending_confirmation = None
            # state.status = AgentStatus.CANCELLED
            self._set_status(state, AgentStatus.CANCELLED)

            self.state_store.save(state)
            log_agent_event(
                "agent.confirmation_declined",
                run_id=run_id,
                trace_id=state.trace_id,
                tool_call_id=request.tool_call_id,
            )
            return state

        log_agent_event(
            "agent.confirmation_approved",
            run_id=run_id,
            trace_id=state.trace_id,
            tool_call_id=request.tool_call_id,
        )

        # Use exact action stored by backend
        definition = self.tool_registry.get(pending.tool_name)

        # Re-check policy after confirmation
        policy_result = self.tool_policy.check(
            definition,
            confirmation_granted=True,
        )

        if policy_result.decision != ToolPolicyDecision.ALLOW:
            raise ToolPolicyError(policy_result.reason)

        # ToolExecutor validates arguments again
        result = self.tool_executor.execute(
            definition,
            pending.arguments,
            context=AgentExecutionContext(
                run_id=state.run_id,
                trace_id=state.trace_id,
                step=state.step,
            ),
        )

        # Record actual tool result
        state.messages.append(
            {
                "role": "tool",
                "tool_call_id": pending.tool_call_id,
                "content": json.dumps(result),
            }
        )

        # Confirmation has been consumed
        state.pending_confirmation = None
        self._set_status(state, AgentStatus.RUNNING)

        # Resume Agent reasoning
        return self._run_loop(state)

    def _set_status(
        self,
        state: AgentState,
        new_status: AgentStatus,
    ) -> None:
        if state.status == new_status:
            return

        state.status = new_status
        self.metrics.increment_agent_status(new_status.value)

    # if status == AgentStatus.COMPLETED:
    #     return response.message["content"]

    # if status == AgentStatus.RUNNING:
    #     continue

    # if status == AgentStatus.FAILED:
    #     raise RuntimeError(f"Agent stopped with status: {status}")


# Version 1
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


# Version 2:
#           ┌───────────────┐
#           │    RUNNING    │
#           └───────┬───────┘
#                   │
#             LLM proposal
#                   │
#      ┌────────────┼────────────┐
#      │            │            │
#    ALLOW      CONFIRM       REJECT
#      │            │            │
#      ▼            ▼            ▼
# execute tool   WAITING      CANCEL/FAIL
#      │            |
#      ▼            |
#   RUNNING         |
#      │            |
#      ▼            |
#   COMPLETED       |
#                   |
#                   |
#                   ▼
# Và riêng nhánh confirmation:

# RUNNING
#    │
#    ▼
# REQUIRE_CONFIRMATION
#    │
#    ▼
# WAITING_FOR_CONFIRMATION
#    │
#    ├──── user confirm ────► RUNNING
#    │                           │
#    │                           ▼
#    │                       execute tool
#    │                           │
#    │                           ▼
#    │                         RUNNING
#    │
#    └──── user cancel ─────► CANCELLED


# General workflow
# LLM proposal
#      ↓
# Policy
#      ↓
# REQUIRE_CONFIRMATION
#      ↓
# Persist Pending Action
#      ↓
# WAITING_FOR_CONFIRMATION
#      ↓
# User Confirm
#      ↓
# Execute EXACT approved action
#      ↓
# Tool Result
#      ↓
# RUNNING
#      ↓
# LLM continues
#      ↓
# FINAL / another TOOL

# ------------------------------------------------------|
# ------------------------------------------------------
# --------------------------- Detail workflow           |
# ------------------------------------------------------
# Human-in-the-loop Agent Runtime                       |
# ------------------------------------------------------

# confirm(request)
#       │
#       ▼
# load AgentState(run_id)
#       │
#       ▼
# check user owns this run
#       │
#       ▼
# status == WAITING_FOR_CONFIRMATION?
#       │
#       ▼
# tool_call_id matches?
#       │
#       ├── NO → reject request
#       │
#       ▼
#   approved?
#    ┌──┴──┐
#   NO     YES
#   │       │
#   ▼       ▼
# CANCEL   re-check policy
#           │
#           ▼
#       validate arguments
#           │
#           ▼
#        execute exact
#           │
#           ▼
#        append result
#           │
#           ▼
#     pending_confirmation=None
#           │
#           ▼
#        RUNNING
#           │
#           ▼
#        continue LLM
