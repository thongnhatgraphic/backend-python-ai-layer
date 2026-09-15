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
from app.eval.reranking.bge_reranker import BGEReranker
from app.eval.reranking.gte_reranker import GTEReranker
from app.eval.reranking.ettin_reranker import EttinReranker

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"

RETRIEVAL_K = 20
FINAL_K = 5


def evaluate():
    print("1. start evaluate")

    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    print("2. dataset loaded")

    evaluation_query_ids = sorted(list(qrels.keys()))

    print("3. query ids:", len(evaluation_query_ids))

    print("4. loading reranker...")
    reranker = EttinReranker()
    print("5. reranker loaded")

    with Session(engine) as session:

        dense_scores = []
        reranked_scores = []

        dense_hits = 0
        dense_misses = 0

        reranked_hits = 0
        reranked_misses = 0

        reranker_rescued = 0
        reranker_regressed = 0

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

            # -------------------------
            # Dense Top-5
            # -------------------------

            dense_top_k = dense_results[:FINAL_K]

            dense_ids = {result.external_id for result in dense_top_k}

            dense_hit = bool(dense_ids & relevant_ids)

            dense_score = recall_at_k(
                [result.external_id for result in dense_top_k],
                relevent_ids=relevant_ids,
                k=FINAL_K,
            )

            dense_scores.append(dense_score)

            if dense_hit:
                dense_hits += 1
            else:
                dense_misses += 1

            # -------------------------
            # Reranking
            # -------------------------

            reranked_results = reranker.rerank(
                query=query_text,
                results=dense_results,
            )

            reranked_top_k = reranked_results[:FINAL_K]

            reranked_ids = {result.external_id for result in reranked_top_k}

            reranked_hit = bool(reranked_ids & relevant_ids)

            reranked_score = recall_at_k(
                [result.external_id for result in reranked_top_k],
                relevent_ids=relevant_ids,
                k=FINAL_K,
            )

            reranked_scores.append(reranked_score)

            if reranked_hit:
                reranked_hits += 1
            else:
                reranked_misses += 1

            # -------------------------
            # Reranker rescued
            # Dense MISS -> Reranker HIT
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

            # -------------------------
            # Reranker regression
            # Dense HIT -> Reranker MISS
            # -------------------------

            elif dense_hit and not reranked_hit:

                reranker_regressed += 1

                print()
                print("========================================")
                print("RERANKER REGRESSION")
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

        dense_recall = sum(dense_scores) / len(dense_scores)

        reranked_recall = sum(reranked_scores) / len(reranked_scores)

        improvement = reranked_recall - dense_recall

        print()
        print("========================================")
        print("FINAL EVALUATION")
        print("========================================")

        print(f"Queries: {len(evaluation_query_ids)}")

        print(f"Dense Recall@{FINAL_K}: " f"{dense_recall:.4%}")

        print(f"Reranked Recall@{FINAL_K}: " f"{reranked_recall:.4%}")

        print(f"Improvement: " f"{improvement:+.4%}")

        print()
        print("Dense:")
        print("  HIT :", dense_hits)
        print("  MISS:", dense_misses)

        print()
        print("Reranked:")
        print("  HIT :", reranked_hits)
        print("  MISS:", reranked_misses)

        print()
        print(
            "Reranker rescued:",
            reranker_rescued,
        )

        print(
            "Reranker regression:",
            reranker_regressed,
        )

        print()
        print("Sanity check:", dense_hits + dense_misses, "queries")

        print("Sanity check reranked:", reranked_hits + reranked_misses, "queries")


if __name__ == "__main__":
    evaluate()
