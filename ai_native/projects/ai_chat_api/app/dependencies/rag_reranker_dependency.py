from app.services.rerankers.ettin_reranker import EttinReranker

model_name = "cross-encoder/ettin-reranker-150m-v1"


def get_rag_reranker() -> EttinReranker:
    return EttinReranker(model_name=model_name)
