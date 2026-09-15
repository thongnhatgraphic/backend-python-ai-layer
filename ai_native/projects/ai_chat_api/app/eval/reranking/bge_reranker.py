from sentence_transformers import CrossEncoder
from app.eval.schema.retrieval_schema import RetrievalResult


class BGEReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.model = CrossEncoder(model_name)

    def rerank(
        self, query: str, results: list[RetrievalResult]
    ) -> list[RetrievalResult]:

        pairs = [[query, result.content] for result in results]

        scores = self.model.predict(
            pairs,
            batch_size=20,
            show_progress_bar=False,
        )

        reranked = [
            result.model_copy(
                update={
                    "score": score,
                }
            )
            for score, result in zip(scores, results)
        ]

        reranked.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return reranked
