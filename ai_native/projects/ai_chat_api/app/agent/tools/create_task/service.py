import time
from app.agent.idempotency.store import IdempotencyStore
from app.agent.idempotency.redis_store import RedisIdempotencyStore
from app.agent.idempotency.heartbeat import LeaseHeartbeat

from app.schemas.reservation_schema import Reservation


class CreateTaskService:
    def __init__(self, store: RedisIdempotencyStore):
        self.store = store
        self.count = 0

    def _wait_for_completion(
        self,
        idempotency_key: str,
        max_wait: float = 6.0,
        initial_interval: float = 0.1,
        max_interval: float = 0.5,
        user: str = None,
    ) -> dict:
        started_at = time.monotonic()
        interval = initial_interval

        while True:
            state = self.store.get(idempotency_key)
            print(f"Operation {user} check state in", state)
            if state is None:
                raise RuntimeError("Idempotency state disappeared")

            if state["status"] == "COMPLETED":
                return state["result"]

            if state["status"] != "PROCESSING":
                raise RuntimeError(f"Unknown idempotency state: {state['status']}")

            elapsed = time.monotonic() - started_at

            if elapsed >= max_wait:
                raise TimeoutError("Timed out waiting for idempotent operation")

            time.sleep(interval)

            interval = min(
                interval * 2,
                max_interval,
            )

    def create(self, title: str, idempotency_key: str, operation: str) -> dict:
        print(f"Operation {operation} is creating task")
        reservation: Reservation = self.store.reserve(
            idempotency_key,
            ttl=2,
        )

        print(f"reservation:{operation}")
        print(f"acquired: =", reservation.acquired)
        print(f"owner_token: =", reservation.owner_token)

        if not reservation.acquired:
            existing = self.store.get(idempotency_key)
            print(f"user {operation} check state", existing)

            if existing is None:
                raise RuntimeError("Idempotency state disappeared")

            if existing["status"] == "COMPLETED":
                return existing["result"]

            if existing["status"] == "PROCESSING":
                return self._wait_for_completion(idempotency_key, user=operation)

            raise RuntimeError(f"Unknown idempotency state: " f"{existing['status']}")

        heartbeat = LeaseHeartbeat(
            store=self.store,
            key=idempotency_key,
            owner_token=reservation.owner_token,
            ttl=10,
            interval=1,
        )

        heartbeat.start()
        print(f"heartbeat started operation: {operation}")
        try:
            time.sleep(5)

            self.count += 1
            result = {
                "task_id": f"task-{self.count}",
                "title": title,
            }

            is_complete = self.store.complete(
                idempotency_key,
                owner_token=reservation.owner_token,
                result=result,
                ttl=30,
            )

            if not is_complete:
                raise RuntimeError("Failed to complete idempotent operation")

            print(f"Operation {operation} created task")
            return result

        finally:
            heartbeat.stop()
