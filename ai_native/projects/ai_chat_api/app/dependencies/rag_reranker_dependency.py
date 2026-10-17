from functools import lru_cache
from app.services.rerankers.ettin_reranker import EttinReranker

model_name = "cross-encoder/ettin-reranker-150m-v1"


@lru_cache(maxsize=1)
def get_rag_reranker() -> EttinReranker:
    return EttinReranker(model_name=model_name)
