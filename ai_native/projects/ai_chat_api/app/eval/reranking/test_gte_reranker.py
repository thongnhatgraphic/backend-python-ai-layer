from app.eval.reranking.gte_reranker import GTEReranker
from app.eval.schema.retrieval_schema import RetrievalResult


def main():

    reranker = GTEReranker()

    query = "1 in 5 million in UK have abnormal PrP positivity."

    documents = [
        "The prevalence of abnormal prion protein was investigated in human appendixes.",
        "This study investigates cancer cell differentiation.",
        "The weather in the United Kingdom was unusual this year.",
    ]

    scores = reranker.rerank(
        query=query,
        results=documents,
    )

    for document, score in zip(documents, scores):
        print()
        print("score:", score)
        print("document:", document)


if __name__ == "__main__":
    main()
