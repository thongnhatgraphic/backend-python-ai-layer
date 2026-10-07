import time
import redis
from app.core.settings import settings
from app.agent.idempotency.store import IdempotencyStore
from app.agent.idempotency.heartbeat import LeaseHeartbeat
from app.agent.idempotency.redis_store import RedisIdempotencyStore

key = "heartbeat-test"

client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

store = RedisIdempotencyStore(client=client)

reservation = store.reserve(
    key,
    ttl=2,
)

print("reservation:", reservation)

heartbeat = LeaseHeartbeat(
    store=store,
    key=key,
    owner_token=reservation.owner_token,
    ttl=2,
    interval=0.6,
)

heartbeat.start()

time.sleep(5)

print(
    "state after 5s:",
    store.get(key),
)
heartbeat.owner_token = "Fake Owner Token"

print("Sleeping 2.5s ...")
time.sleep(2.5)

heartbeat.stop()

print(
    "state after heartbeat stopped:",
    store.get(key),
)
