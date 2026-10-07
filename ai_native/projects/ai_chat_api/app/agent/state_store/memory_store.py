from app.agent.state import AgentState


class InMemoryAgentStateStore:
    def __init__(self):
        self._states: dict[str, AgentState] = {}

    def save(self, state: AgentState) -> None:
        self._states[state.run_id] = state.model_copy(deep=True)

    def get(self, run_id: str) -> AgentState | None:
        state = self._states.get(run_id)

        if state is None:
            return None

        return state.model_copy(deep=True)

    def delete(self, run_id: str) -> None:
        self._states.pop(run_id, None)
