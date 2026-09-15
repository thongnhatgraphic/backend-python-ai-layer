from app.services.token_counter import TokenCounter


class PlannerContextHistorySelector:
    def __init__(
        self,
        token_counter: TokenCounter,
        max_tokens: int,
    ):
        self.token_counter = token_counter
        self.max_tokens = max_tokens

    def select(
        self,
        history: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        selected = []
        total_token = 0

        for message in reversed(history):
            tokens = self.token_counter.count(message["content"])

            if total_token + tokens > self.max_tokens:
                break

            selected.append(message)
            total_token += tokens

        selected.reverse()

        return selected
