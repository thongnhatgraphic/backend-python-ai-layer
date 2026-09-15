from statistics import mean
from uuid import UUID

from app.tests.evaluation.reranker_eval_dataset import (
    EVALUATION_DATASET,
)
from app.tests.test_semantic_search import (
    embed,
    semantic_search,
)

USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")

CANDIDATE_K_VALUES = [5, 10, 15, 19]


def recall_at_k(
    retrieved_ids: set[str],
    relevant_ids: set[str],
) -> float:
    if not relevant_ids:
        return 0.0

    hits = retrieved_ids & relevant_ids

    return len(hits) / len(relevant_ids)


def main():
    print("=" * 80)
    print("CANDIDATE K CALIBRATION")
    print("=" * 80)

    results = {k: [] for k in CANDIDATE_K_VALUES}

    no_relevant_queries = 0

    for index, item in enumerate(
        EVALUATION_DATASET,
        start=1,
    ):
        query = item["query"]
        relevant_ids = item["relevant_ids"]

        if not relevant_ids:
            no_relevant_queries += 1
            continue

        query_embedding = embed(query)

        print(f"\nQuery {index}: {query}")

        for k in CANDIDATE_K_VALUES:
            candidates = semantic_search(
                USER_ID,
                query_embedding,
                limit=k,
            )

            retrieved_ids = {str(result.memory.id) for result in candidates}

            recall = recall_at_k(
                retrieved_ids,
                relevant_ids,
            )

            results[k].append(recall)

            print(f"  K={k:<2} " f"Candidate Recall={recall:.3f}")

    print("\n")
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"{'K':>5}" f"{'Avg Recall':>15}" f"{'Queries':>12}")

    print("-" * 40)

    for k in CANDIDATE_K_VALUES:
        recalls = results[k]

        average_recall = mean(recalls) if recalls else 0.0

        print(f"{k:>5}" f"{average_recall:>15.3f}" f"{len(recalls):>12}")

    print(f"\nIgnored no-relevant queries: " f"{no_relevant_queries}")


if __name__ == "__main__":
    main()
