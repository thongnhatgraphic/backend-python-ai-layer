from app.core.settings import settings
from app.services.token_counter import TokenCounter

counter = TokenCounter(model_name=settings.TOKENIZER_MODEL)


def get_token_counter() -> TokenCounter:
    return counter
