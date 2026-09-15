from sentence_transformers import CrossEncoder

from app.schemas.retrieval_schema import RetrievalResult


class EttinReranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ettin-reranker-150m-v1",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:

        pairs = [[query, result.content] for result in results]

        scores = self.model.predict(
            pairs,
            batch_size=len(pairs),
            show_progress_bar=False,
        )

        reranked = [
            result.model_copy(
                update={
                    "score": float(score),
                }
            )
            for result, score in zip(results, scores)
        ]

        reranked.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return reranked
