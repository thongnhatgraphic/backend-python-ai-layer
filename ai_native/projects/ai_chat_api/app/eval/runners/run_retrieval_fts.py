import json
from pathlib import Path

from sqlmodel import Session

from app.eval.datasets.scifact.qrels_loader import load_qrels
from app.eval.datasets.scifact.query_loader import load_queries
from app.eval.metrics.retrieval_metrics import recall_at_k
from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)

from app.eval.retrieval.lexical_search import lexical_search

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"

K = 20


def evaluate():
    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    evaluation_query_ids = sorted(qrels.keys())

    with Session(engine) as session:

        dense_scores = []
        lexical_scores = []

        dense_hit_lexical_hit = 0
        dense_hit_lexical_miss = 0
        dense_miss_lexical_hit = 0
        dense_miss_lexical_miss = 0

        for query_id in evaluation_query_ids:

            query_text = queries[query_id]

            relevant_ids = set(qrels[query_id])

            # -------------------------
            # Dense Retrieval
            # -------------------------

            query_embedding = embedding_service.embed_text(query_text)

            with session.begin():
                dense_results = search_by_embedding(
                    session=session,
                    query_embedding=query_embedding,
                    limit=K,
                    ef_search=40,
                )

                dense_ids = {result.external_id for result in dense_results}

                dense_score = recall_at_k(
                    retrieved_ids=[result.external_id for result in dense_results],
                    relevent_ids=relevant_ids,
                    k=K,
                )

                dense_scores.append(dense_score)

                # -------------------------
                # Lexical Retrieval
                # -------------------------

                lexical_results = lexical_search(
                    session=session,
                    query=query_text,
                    limit=K,
                )

                lexical_ids = {result.external_id for result in lexical_results}

                lexical_score = recall_at_k(
                    retrieved_ids=[result.external_id for result in lexical_results],
                    relevent_ids=relevant_ids,
                    k=K,
                )

                lexical_scores.append(lexical_score)

                # -------------------------
                # Dense MISS / Lexical HIT
                # -------------------------

                dense_hit = bool(dense_ids & relevant_ids)

                lexical_hit = bool(lexical_ids & relevant_ids)

                if dense_hit and lexical_hit:
                    dense_hit_lexical_hit += 1

                elif dense_hit and not lexical_hit:
                    dense_hit_lexical_miss += 1

                elif not dense_hit and lexical_hit:
                    dense_miss_lexical_hit += 1

                else:
                    dense_miss_lexical_miss += 1

        print()
        print(f"Dense Recall@{K}: " f"{sum(dense_scores) / len(dense_scores):.4%}")

        print(
            f"Lexical Recall@{K}: " f"{sum(lexical_scores) / len(lexical_scores):.4%}"
        )
        print(
            "Dense miss / Lexical hit:",
            dense_miss_lexical_hit,
        )

        print("Dense HIT + Lexical HIT:", dense_hit_lexical_hit)
        print("Dense HIT + Lexical MISS:", dense_hit_lexical_miss)
        print("Dense MISS + Lexical HIT:", dense_miss_lexical_hit)
        print("Dense MISS + Lexical MISS:", dense_miss_lexical_miss)


if __name__ == "__main__":
    evaluate()
