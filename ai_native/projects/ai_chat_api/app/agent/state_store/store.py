from typing import Protocol

from app.agent.state import AgentState


class AgentStateStore(Protocol):

    def save(self, state: AgentState) -> None: ...

    def get(self, run_id: str) -> AgentState | None: ...

    def delete(self, run_id: str) -> None: ...
