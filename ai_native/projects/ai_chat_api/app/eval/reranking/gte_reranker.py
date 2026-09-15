from sentence_transformers import CrossEncoder

from app.eval.schema.retrieval_schema import RetrievalResult


class GTEReranker:

    def __init__(
        self,
        model_name: str = "Alibaba-NLP/gte-multilingual-reranker-base",
    ):
        self.model = CrossEncoder(
            model_name,
            trust_remote_code=True,
        )

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
                },
            )
            for result, score in zip(results, scores)
        ]

        reranked.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return reranked
