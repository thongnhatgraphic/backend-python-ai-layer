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

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"

K_VALUES = [20]


def evaluate():
    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    evaluation_query_ids = sorted(qrels.keys())
    print("\n query ids \n", evaluation_query_ids)

    totals = {k: 0.0 for k in K_VALUES}
    print("\n totals \n", totals)

    evaluated_queries = 0

    with Session(engine) as session:

        for query_id in evaluation_query_ids:

            query = queries[query_id]  # text query
            relevant_ids = qrels[query_id]  # ground truth

            query_embedding = embedding_service.embed_text(query)

            results = search_by_embedding(
                session=session,
                query_embedding=query_embedding,
                limit=max(K_VALUES),
                ef_search=100,
            )

            retrieved_ids = [result.external_id for result in results]

            for k in K_VALUES:
                score = recall_at_k(
                    retrieved_ids=retrieved_ids,
                    relevent_ids=set(relevant_ids),
                    k=k,
                )
                totals[k] += score

            evaluated_queries += 1

            if evaluated_queries % 25 == 0:
                print(
                    f"Evaluated "
                    f"{evaluated_queries}/"
                    f"{len(evaluation_query_ids)} queries"
                )
                print("totals", totals)

    print("\n=== Retrieval Evaluation ===")

    for k in K_VALUES:
        mean_recall = totals[k] / evaluated_queries

        print(f"Recall@{k}: " f"{mean_recall:.4f} " f"({mean_recall * 100:.2f}%)")


if __name__ == "__main__":
    evaluate()


# === Retrieval Evaluation ===
# Recall@20: 0.8155 (81.55%) ef_search = 10
# Recall@20: 0.8770 (87.70%) ef_search = 20
# Recall@20: 0.8903 (89.03%) ef_search = 40
# Recall@20: 0.8970 (89.70%) ef_search = 80
# Recall@20: 0.8970 (89.70%) ef_search = 100
