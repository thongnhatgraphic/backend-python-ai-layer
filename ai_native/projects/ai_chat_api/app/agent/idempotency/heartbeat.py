import threading
import time
import logging
from app.agent.idempotency.redis_store import RedisIdempotencyStore

# | Tình huống                         | A                            | B                    | Nguy cơ               | Cách xử lý                           |
# | ---------------------------------- | ---------------------------- | -------------------- | --------------------- | ------------------------------------ |
# | **1. GET → CREATE → SAVE**         | thấy None                    | thấy None            | 2 side effects        | `SET NX`                             |
# | **2. B đến khi A đang PROCESSING** | đang execute                 | thấy PROCESSING      | B execute lại         | Poll / in-flight dedup               |
# | **3. Complete GET → CHECK → SET**  | check owner                  | state có thể đổi     | stale write           | Atomic Lua                           |
# | **4. TTL hết khi A đang chạy**     | vẫn execute                  | claim key mới        | 2 owners              | Heartbeat / lease                    |
# | **5. A chết giữa execution**       | crash                        | chưa thể claim       | PROCESSING bị treo    | TTL                                  |
# | **6. Retry sau timeout**           | side effect có thể đã xảy ra | retry cùng operation | duplicate side effect | Same idempotency key + cached result |

# | Khái niệm       | Câu hỏi nó giải quyết                                           |
# | --------------- | --------------------------------------------------------------- |
# | `SET NX`        | **Ai giành được ownership?**                                    |
# | Ownership token | **Ai có quyền complete/renew?**                                 |
# | TTL             | **Nếu owner chết thì bao giờ giải phóng?**                      |
# | Heartbeat       | **Owner còn sống thì làm sao giữ lease?**                       |
# | Polling         | **Operation đã có worker chạy thì execution khác chờ thế nào?** |
# | Retry           | **Execution thất bại thì có nên execute lại không?**            |
# | Idempotency key | **Các retry này có phải cùng một logical operation không?**     |
# | Atomic Lua      | **Làm sao check + update không bị race?**                       |

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


class LeaseHeartbeat:
    def __init__(
        self,
        store: RedisIdempotencyStore,
        key: str,
        owner_token: str,
        ttl: int,
        interval: float,
    ):
        self.store = store
        self.key = key
        self.owner_token = owner_token
        self.ttl = ttl
        self.interval = interval

        self._stop_event = threading.Event()
        self._lost_ownership = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            raise RuntimeError("Heartbeat already started")

        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )
        self._thread.start()

    def lost_ownership(self) -> None:
        self._lost_ownership.set()

    def stop(self) -> None:
        self._stop_event.set()

        if self._thread is not None:
            self._thread.join()

    def _run(self) -> None:
        while not self._stop_event.wait(self.interval):
            success = self.store.renew(
                key=self.key,
                owner_token=self.owner_token,
                ttl=self.ttl,
            )
            print("renewed:", success)
            if not success:
                self.lost_ownership()
                logger.warning(
                    "Heartbeat lost ownership: key=%s",
                    self.key,
                )
                break

            logger.info(
                "Heartbeat renewed lease: key=%s",
                self.key,
            )
