from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

import torch
import math
import time
from statistics import mean
from uuid import UUID


from app.tests.evaluation.reranker_eval_dataset import (
    EVALUATION_DATASET,
)
from app.tests.test_semantic_search import (
    embed,
    semantic_search,
)

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")

# Stage 1
VECTOR_SEARCH_K = 15

# Các final limits sẽ thử
RERANK_LIMITS = [3, 5, 7]

# BGE direct dùng raw logits.
# Chúng ta sẽ thu thập score thực tế rồi tạo threshold từ score distribution.
torch.set_num_threads(12)


# ============================================================
# Model
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()


# ============================================================
# Metrics
# ============================================================


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:

    if not retrieved_ids:
        return 0.0

    hits = set(retrieved_ids) & relevant_ids

    return len(hits) / len(retrieved_ids)


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float:

    if not relevant_ids:
        return 0.0

    hits = set(retrieved_ids) & relevant_ids

    return len(hits) / len(relevant_ids)


def f1_score(
    precision: float,
    recall: float,
) -> float:

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def ndcg_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:

    retrieved_ids = retrieved_ids[:k]

    if not relevant_ids:
        return 0.0

    dcg = 0.0

    for rank, memory_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        relevance = 1 if memory_id in relevant_ids else 0

        dcg += relevance / math.log2(rank + 1)

    ideal_count = min(
        len(relevant_ids),
        k,
    )

    idcg = 0.0

    for rank in range(
        1,
        ideal_count + 1,
    ):
        idcg += 1 / math.log2(rank + 1)

    if idcg == 0:
        return 0.0

    return dcg / idcg


# ============================================================
# BGE scoring
# ============================================================


def rerank(
    query: str,
    candidates,
):
    pairs = [
        [
            query,
            candidate.memory.content,
        ]
        for candidate in candidates
    ]

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512,
    )

    with torch.no_grad():

        scores = (
            model(
                **inputs,
                return_dict=True,
            )
            .logits.view(-1)
            .float()
            .tolist()
        )

    results = []

    for candidate, score in zip(
        candidates,
        scores,
    ):
        results.append(
            {
                "id": str(candidate.memory.id),
                "content": candidate.memory.content,
                "score": score,
            }
        )

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True,
    )


# ============================================================
# Prepare evaluation data
# ============================================================


def prepare_evaluation():

    evaluation_results = []

    all_scores = []

    for index, item in enumerate(
        EVALUATION_DATASET,
        start=1,
    ):
        query = item["query"]
        relevant_ids = item["relevant_ids"]

        embedding = embed(query)

        candidates = semantic_search(
            USER_ID,
            embedding,
            limit=VECTOR_SEARCH_K,
        )

        reranked = rerank(
            query,
            candidates,
        )

        for result in reranked:
            all_scores.append(result["score"])

        evaluation_results.append(
            {
                "index": index,
                "query": query,
                "relevant_ids": relevant_ids,
                "reranked": reranked,
            }
        )

    return evaluation_results, all_scores


# ============================================================
# Threshold candidates
# ============================================================


def build_thresholds(
    all_scores: list[float],
):
    """
    Use observed score distribution instead of
    guessing a universal threshold.

    Add a little padding around min/max.
    """

    unique_scores = sorted(
        set(all_scores),
        reverse=True,
    )

    if not unique_scores:
        return []

    thresholds = []

    # Slightly below the lowest score
    thresholds.append(unique_scores[-1] - 0.001)

    # Every observed score itself
    thresholds.extend(unique_scores)

    # Slightly above the highest score
    thresholds.append(unique_scores[0] + 0.001)

    return sorted(
        set(thresholds),
        reverse=True,
    )


# ============================================================
# Evaluate one threshold
# ============================================================


def evaluate_threshold(
    evaluation_results,
    threshold: float,
    limit: int,
):
    precisions = []
    recalls = []
    f1s = []
    ndcgs = []

    num_memories = []
    no_relevant_queries = 0
    false_positive_queries = 0

    for item in evaluation_results:

        relevant_ids = item["relevant_ids"]

        filtered = [
            result for result in item["reranked"] if result["score"] >= threshold
        ]

        filtered = filtered[:limit]

        retrieved_ids = [result["id"] for result in filtered]

        if not relevant_ids:
            no_relevant_queries += 1

            if retrieved_ids:
                false_positive_queries += 1

        precision = precision_at_k(
            retrieved_ids,
            relevant_ids,
        )

        recall = recall_at_k(
            retrieved_ids,
            relevant_ids,
        )

        f1 = f1_score(
            precision,
            recall,
        )

        ndcg = ndcg_at_k(
            retrieved_ids,
            relevant_ids,
            limit,
        )

        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
        ndcgs.append(ndcg)

        num_memories.append(len(retrieved_ids))

    return {
        "threshold": threshold,
        "precision": mean(precisions),
        "recall": mean(recalls),
        "f1": mean(f1s),
        "ndcg": mean(ndcgs),
        "avg_memories": mean(num_memories),
        "false_positive_queries": false_positive_queries,
        "no_relevant_queries": no_relevant_queries,
    }


# ============================================================
# Threshold calibration
# ============================================================


def calibrate_threshold(
    evaluation_results,
    thresholds,
    limit: int,
):
    results = []

    for threshold in thresholds:

        result = evaluate_threshold(
            evaluation_results,
            threshold,
            limit,
        )

        results.append(result)

    return results


# ============================================================
# Print threshold results
# ============================================================


def print_threshold_results(
    results,
    limit: int,
):
    print("\n")
    print("=" * 90)
    print(f"THRESHOLD CALIBRATION | LIMIT={limit}")
    print("=" * 90)

    print(
        f"{'Threshold':>12}"
        f"{'Precision':>12}"
        f"{'Recall':>12}"
        f"{'F1':>12}"
        f"{'NDCG':>12}"
        f"{'AvgMem':>12}"
        f"{'FP queries':>12}"
    )

    print("-" * 90)

    for result in results:

        print(
            f"{result['threshold']:12.6f}"
            f"{result['precision']:12.3f}"
            f"{result['recall']:12.3f}"
            f"{result['f1']:12.3f}"
            f"{result['ndcg']:12.3f}"
            f"{result['avg_memories']:12.2f}"
            f"{result['false_positive_queries']:12d}"
        )


# ============================================================
# Select threshold
# ============================================================


def select_threshold(
    results,
    minimum_recall: float = 0.80,
):
    """
    Strategy:

    1. Keep thresholds with recall >= minimum_recall.
    2. Among those, maximize F1.
    3. If tied, prefer higher threshold.
    """

    valid = [result for result in results if result["recall"] >= minimum_recall]

    if not valid:
        return None

    return max(
        valid,
        key=lambda result: (
            result["f1"],
            result["threshold"],
        ),
    )


# ============================================================
# Main
# ============================================================


def main():

    print("Preparing evaluation dataset...")

    evaluation_results, all_scores = prepare_evaluation()

    print(f"Queries: " f"{len(evaluation_results)}")

    print(f"Total reranker scores: " f"{len(all_scores)}")

    print(f"Min score: " f"{min(all_scores):.6f}")

    print(f"Max score: " f"{max(all_scores):.6f}")

    thresholds = build_thresholds(all_scores)

    print(f"Threshold candidates: " f"{len(thresholds)}")

    # --------------------------------------------------------
    # Threshold calibration
    # --------------------------------------------------------

    all_limit_results = {}

    for limit in RERANK_LIMITS:

        results = calibrate_threshold(
            evaluation_results,
            thresholds,
            limit,
        )

        all_limit_results[limit] = results

        print_threshold_results(
            results,
            limit,
        )

        best = select_threshold(
            results,
            minimum_recall=0.80,
        )

        print("\nBest threshold:")

        if best:
            print(best)
        else:
            print("No threshold satisfies " "Recall >= 0.80")


if __name__ == "__main__":
    main()
