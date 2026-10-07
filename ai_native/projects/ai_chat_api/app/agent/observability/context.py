from dataclasses import dataclass


@dataclass
class AgentExecutionContext:
    run_id: str
    trace_id: str
    step: int
