import random
from app.agent.errors.tool_errors import ToolTransientError, ToolTimeoutError


class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 0.2,
        max_delay: float = 2.0,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")

        if base_delay < 0:
            raise ValueError("base_delay must be >= 0")

        if max_delay < base_delay:
            raise ValueError("max_delay must be >= base_delay")

        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay

    def should_retry(
        self,
        error: Exception,
        attempt: int,
    ) -> bool:
        if attempt >= self.max_attempts:
            return False

        return isinstance(
            error,
            (
                ToolTransientError,
                ToolTimeoutError,
            ),
        )

    def get_delay(self, attempt: int) -> float:
        exponential_delay = self.base_delay * (2 ** (attempt - 1))

        capped_delay = min(
            exponential_delay,
            self.max_delay,
        )

        return random.uniform(
            0,
            capped_delay,
        )
