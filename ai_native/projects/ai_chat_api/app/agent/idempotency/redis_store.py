# 1. Ai sở hữu operation?
#    → SET NX

# 2. Owner còn sống không?
#    → Heartbeat + TTL

# 3. Owner có quyền update state không?
#    → Owner token + atomic check

# 4. Có worker khác đang xử lý không?
#    → Poll / in-flight deduplication

# 5. Execution fail thì có execute lại không?
#    → RetryPolicy

# 6. Retry có gây duplicate side effect không?
#    → Idempotency

import json
import redis
import secrets
from app.schemas.reservation_schema import Reservation


class RedisIdempotencyStore:
    def __init__(self, client: redis.Redis):
        self.client = client

    def _key(self, key: str) -> str:
        return f"agent:idempotency:{key}"

    def reserve(self, key: str, ttl: int) -> Reservation:
        owner_token = secrets.token_urlsafe(32)

        value = json.dumps(
            {
                "status": "PROCESSING",
                "owner_token": owner_token,
            }
        )

        acquired = self.client.set(
            self._key(key),
            value,
            nx=True,
            ex=ttl,
        )

        if not acquired:
            return Reservation(
                acquired=False,
            )

        return Reservation(
            acquired=True,
            owner_token=owner_token,
        )

    def get(
        self,
        key: str,
    ) -> dict | None:

        value = self.client.get(self._key(key))

        if value is None:
            return None

        return json.loads(value)

    def complete(
        self,
        key: str,
        owner_token: str,
        result: dict,
        ttl: int,
    ) -> bool:

        script = """
        local current = redis.call("GET", KEYS[1])

        if not current then
            return 0
        end

        local data = cjson.decode(current)

        if data.owner_token ~= ARGV[1] then
            return 0
        end

        local completed = cjson.encode({
            status = "COMPLETED",
            result = cjson.decode(ARGV[2])
        })

        redis.call(
            "SET",
            KEYS[1],
            completed,
            "EX",
            ARGV[3]
        )

        return 1
        """

        result_json = json.dumps(result)

        response = self.client.eval(
            script,
            1,
            self._key(key),
            owner_token,
            result_json,
            ttl,
        )

        return bool(response)

    def renew(self, key: str, owner_token: str, ttl: int) -> bool:
        script = """
        local current = redis.call("GET", KEYS[1])

        if not current then
            return 0
        end

        local data = cjson.decode(current)

        if data.owner_token ~= ARGV[1] then
            return 0
        end

        redis.call("EXPIRE", KEYS[1], ARGV[2])

        return 1

    """

        response = self.client.eval(
            script,
            1,
            self._key(key),
            owner_token,
            ttl,
        )
        return bool(response)
