from app.schemas.retrieval_schema import RetrievalResult


class RelevanceGate:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def filter(
        self,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:

        return [result for result in results if result.score >= self.threshold]
