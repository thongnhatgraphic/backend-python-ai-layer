from pathlib import Path

from sqlmodel import Session

from app.eval.datasets.scifact.qrels_loader import load_qrels
from app.eval.datasets.scifact.query_loader import load_queries
from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)
from app.eval.reranking.bge_reranker import BGEReranker
from app.eval.reranking.ettin_reranker import EttinReranker

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"

RETRIEVAL_K = 20
FINAL_K = 5


def evaluate():

    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    # evaluation_query_ids = sorted(list(qrels.keys()))[:20] Reranker rescued: 1 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[20:40] Reranker rescued: 1 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[40:60] Reranker rescued: 2 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[60:80] Reranker rescued: 1 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[80:100]Reranker rescued: 0 / 19
    # evaluation_query_ids = sorted(list(qrels.keys()))[100:120] Reranker rescued: 0 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[120:140] Reranker rescued: 1 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[140:160] Reranker rescued: 2 / 20
    # evaluation_query_ids = sorted(list(qrels.keys()))[160:200] Reranker rescued: 1 / 40
    evaluation_query_ids = sorted(list(qrels.keys()))
    reranker = EttinReranker()

    reranker_rescued = 0
    number_of_queries = 0

    with Session(engine) as session:
        print("Starting evaluation...")
        for query_id in evaluation_query_ids:

            query_text = queries[query_id]
            relevant_ids = set(qrels[query_id])

            # -------------------------
            # Dense Retrieval Top-20
            # -------------------------

            query_embedding = embedding_service.embed_text(query_text)

            dense_results = search_by_embedding(
                session=session,
                query_embedding=query_embedding,
                limit=RETRIEVAL_K,
                ef_search=40,
            )

            dense_top_k = dense_results[:FINAL_K]

            dense_ids = {result.external_id for result in dense_top_k}

            dense_hit = bool(dense_ids & relevant_ids)

            # -------------------------
            # Reranking
            # -------------------------

            reranked_results = reranker.rerank(
                query=query_text,
                results=dense_results,
            )
            number_of_queries += 1
            print("Complete Reranking of 1 query...")
            print("Query", number_of_queries, " of", len(evaluation_query_ids))
            reranked_top_k = reranked_results[:FINAL_K]

            reranked_ids = {result.external_id for result in reranked_top_k}

            reranked_hit = bool(reranked_ids & relevant_ids)

            # -------------------------
            # Reranker rescued query
            # -------------------------

            if not dense_hit and reranked_hit:

                reranker_rescued += 1

                print()
                print("========================================")
                print("RERANKER RESCUED")
                print("query_id:", query_id)
                print("query:", query_text)
                print("ground_truth:", relevant_ids)

                print("\nDense Top-5:")
                for rank, result in enumerate(
                    dense_top_k,
                    start=1,
                ):
                    print(
                        rank,
                        result.external_id,
                        result.score,
                        result.title,
                    )

                print("\nReranked Top-5:")
                for rank, result in enumerate(
                    reranked_top_k,
                    start=1,
                ):
                    print(
                        rank,
                        result.external_id,
                        result.score,
                        result.title,
                    )

        print()
        print("========================================")
        print(
            "Reranker rescued:",
            reranker_rescued,
            "/",
            len(evaluation_query_ids),
        )


if __name__ == "__main__":
    evaluate()
