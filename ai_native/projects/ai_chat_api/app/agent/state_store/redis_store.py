import json
import redis
from app.agent.state import AgentState
from app.core.settings import settings


class RedisAgentStateStore:
    def __init__(
        self,
        client: redis.Redis,
        ttl: int = 3600,
    ):
        self.client = client
        self.ttl = ttl

    def _key(self, run_id: str) -> str:
        return f"agent:state:{run_id}"

    def save(self, state: AgentState) -> None:
        payload = state.model_dump(mode="json")

        print("\n <<<<<<<<payload>>>>>>>>> \n", payload)

        serialized = json.dumps(payload)

        print("\n <<<<<<<<serialized>>>>>>>>> \n", serialized)

        self.client.set(
            self._key(state.run_id),
            json.dumps(payload),
            ex=self.ttl,
        )

        print("\n Save successful \n", self._key(state.run_id))
        print("\n Get AgentState \n", self.get(state.run_id))

    def get(self, run_id: str) -> AgentState | None:
        value = self.client.get(self._key(run_id))

        if value is None:
            return None

        payload = json.loads(value)

        return AgentState.model_validate(payload)

    def delete(self, run_id: str) -> None:
        self.client.delete(self._key(run_id))
