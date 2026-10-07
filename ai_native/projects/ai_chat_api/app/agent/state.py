from pydantic import BaseModel, Field
from enum import Enum
from uuid import uuid4


class AgentStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STEP_LIMIT_EXCEEDED = "STEP_LIMIT_EXCEEDED"

    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"
    CANCELLED = "CANCELLED"


class ResponseType(str, Enum):
    FINAL = "FINAL"
    TOOL_CALL = "TOOL_CALL"
    NO_PROGRESS = "NO_PROGRESS"


class PendingConfirmation(BaseModel):
    tool_call_id: str
    tool_name: str
    arguments: dict
    reason: str


class AgentState(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    run_id: str = Field(default_factory=lambda: str(uuid4()))

    user_message: str
    messages: list[dict]

    step: int = 0
    status: AgentStatus = AgentStatus.RUNNING
    max_steps: int = 3

    no_progress_retries: int = 0
    max_no_progress_retries: int = 1

    pending_confirmation: PendingConfirmation | None = None
