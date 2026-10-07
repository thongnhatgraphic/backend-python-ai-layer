#                   IdempotencyStore
#                          │
#               ┌──────────┴──────────┐
#               ↓                     ↓
#           reserve()             get_result()
#               │                     │
#         atomic SET NX               │
#               │                     │
#          ┌────┴────┐                │
#          ↓         ↓                ↓
#        won       already         COMPLETED
#          │        exists             │
#          ↓           │              ↓
#       execute       stop       return result
#          │
#          ↓
#       side effect
#          │
#          ↓
#    mark COMPLETED
from typing import Protocol


class IdempotencyStore(Protocol):

    def get(self, key: str) -> dict | None: ...

    def save(self, key: str, result: dict) -> None: ...

    def reserve(self, key: str, ttl: int) -> bool: ...

    def complete(
        self,
        key: str,
        result: dict,
        ttl: int,
    ) -> None: ...
