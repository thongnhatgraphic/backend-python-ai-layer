#          ContextBudget
#               │
#               ▼
#        available tokens
#               │
#               ▼
#      ContextAllocator
#         /      |      \
#        /       |       \
#    Memory      RAG    History
#        \       |       /
#         \      |      /
#               ▼
#         ContextBuilder


class ContextBudget:
    def __init__(
        self,
        context_window: int,
        reserved_output_tokens: int,
        safety_margin_tokens: int,
    ):
        if context_window <= 0:
            raise ValueError("context_window must be greater than 0")

        if reserved_output_tokens < 0:
            raise ValueError("reserved_output_tokens cannot be negative")

        if safety_margin_tokens < 0:
            raise ValueError("safety_margin_tokens cannot be negative")

        if reserved_output_tokens + safety_margin_tokens >= context_window:
            raise ValueError(
                "Reserved output and safety margin must be smaller "
                "than context window"
            )

        self.context_window = context_window
        self.reserved_output_tokens = reserved_output_tokens
        self.safety_margin_tokens = safety_margin_tokens

    @property
    def max_input_tokens(self) -> int:
        return (
            self.context_window
            - self.reserved_output_tokens
            - self.safety_margin_tokens
        )
