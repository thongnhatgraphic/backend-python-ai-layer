import threading
import redis

from app.core.settings import settings
from app.agent.idempotency.store import IdempotencyStore
from app.agent.tools.create_task.service import CreateTaskService
from app.agent.idempotency.redis_store import RedisIdempotencyStore

# store = IdempotencyStore()


client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

store = RedisIdempotencyStore(client=client)

print("count:", store.get("operation-123"))

service = CreateTaskService(store)

results = []


def worker1():
    result = service.create(
        title="Hello World 1", idempotency_key="operation-2", operation="A"
    )
    results.append(result)


def worker2():
    result = service.create(
        title="Hello World 2", idempotency_key="operation-2", operation="B"
    )
    results.append(result)


thread1 = threading.Thread(target=worker1)
thread2 = threading.Thread(target=worker2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("results:", results)

print("count:", service.count)
