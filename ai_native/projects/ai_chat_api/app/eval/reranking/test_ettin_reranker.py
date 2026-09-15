from app.eval.reranking.ettin_reranker import EttinReranker
from app.eval.schema.retrieval_schema import RetrievalResult

from sqlmodel import Session

from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)

RETRIEVAL_K = 20


def main():

    reranker = EttinReranker()

    query = "1 in 5 million in UK have abnormal PrP positivity."

    with Session(engine) as session:
        query_embedding = embedding_service.embed_text(query)
        print("query_embedding", len(query_embedding))

        documents = search_by_embedding(
            session=session,
            query_embedding=query_embedding,
            limit=RETRIEVAL_K,
            ef_search=40,
        )

    scores = reranker.rerank(
        query=query,
        results=documents,
    )

    for document, score in zip(documents, scores):
        print()
        print("score:", score.score)
        print("document:", document.external_id)


if __name__ == "__main__":
    main()
