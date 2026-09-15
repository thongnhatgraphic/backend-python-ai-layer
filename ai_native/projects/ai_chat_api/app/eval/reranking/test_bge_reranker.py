from app.eval.reranking.bge_reranker import BGEReranker


def main():

    reranker = BGEReranker()

    query = "1 in 5 million in UK have abnormal PrP positivity."

    documents = [
        "The prevalence of abnormal prion protein was investigated in human appendixes.",
        "This study investigates cancer cell differentiation.",
        "The weather in the United Kingdom was unusual this year.",
    ]

    scores = reranker.rerank(
        query=query,
        documents=documents,
    )

    for document, score in zip(documents, scores):
        print()
        print("score:", score)
        print("document:", document)


if __name__ == "__main__":
    main()
