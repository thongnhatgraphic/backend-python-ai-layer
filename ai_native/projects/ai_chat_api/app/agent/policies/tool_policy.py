from enum import Enum
from pydantic import BaseModel
from app.agent.definitions.tool_definition import ToolDefinition


class ToolPolicyDecision(str, Enum):
    ALLOW = "ALLOW"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    REJECT = "REJECT"


class ToolPolicyResult(BaseModel):
    decision: ToolPolicyDecision
    reason: str


class ToolPolicy:
    def __init__(self):
        pass

    def check(
        self,
        tool: ToolDefinition,
        *,
        confirmation_granted: bool = False,
    ) -> ToolPolicyResult:
        if tool.require_confirmation and not confirmation_granted:
            return ToolPolicyResult(
                decision=ToolPolicyDecision.REQUIRE_CONFIRMATION,
                reason="Tool requires user confirmation before execution.",
            )

        return ToolPolicyResult(
            decision=ToolPolicyDecision.ALLOW,
            reason="Tool is allowed to execute automatically.",
        )
