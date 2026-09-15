from sqlmodel import Session

from app.eval.datasets.scifact.qrels_loader import load_qrels
from app.eval.datasets.scifact.query_loader import load_queries
from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)
from app.eval.reranking.bge_reranker import BGEReranker

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"


def main():
    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    query_id = sorted(list(qrels.keys()))[0]
    # query_id = sorted(qrels.keys())[0]
    print("query_id", query_id)
    query_text = queries[query_id]

    reranker = BGEReranker()

    with Session(engine) as session:

        query_embedding = embedding_service.embed_text(query_text)

        dense_results = search_by_embedding(
            session=session,
            query_embedding=query_embedding,
            limit=20,
            ef_search=40,
        )

        print("\nQuery:")
        print(query_text)

        print("\n--- Dense Top-20 ---")

        for rank, result in enumerate(
            dense_results,
            start=1,
        ):
            print(
                rank,
                result.external_id,
                result.score,
                result.title,
            )

        reranked_results = reranker.rerank(
            query=query_text,
            results=dense_results,
        )

        print("\n--- Reranked Top-20 ---")

        for rank, result in enumerate(
            reranked_results,
            start=1,
        ):
            print(
                rank,
                result.external_id,
                result.score,
                result.title,
            )


if __name__ == "__main__":
    main()
