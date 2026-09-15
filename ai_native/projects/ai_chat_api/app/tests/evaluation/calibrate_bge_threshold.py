import math
from statistics import mean

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
from uuid import UUID


from app.tests.evaluation.reranker_eval_dataset import (
    EVALUATION_DATASET,
)
from app.tests.test_semantic_search import (
    embed,
    semantic_search,
)

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

VECTOR_SEARCH_K = 15

RERANK_LIMITS = [3, 5, 7]
USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")
THRESHOLDS = [
    2.0,
    1.0,
    0.5,
    0.0,
    -0.5,
    -1.0,
    -1.5,
    -2.0,
    -2.5,
    -3.0,
    -3.5,
    -4.0,
    -4.5,
    -5.0,
    -5.5,
    -6.0,
    -6.5,
    -7.0,
    -7.5,
    -8.0,
    -8.5,
    -9.0,
    -9.5,
    -10.0,
]

torch.set_num_threads(12)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()


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


def prepare_evaluation():

    results = []

    for item in EVALUATION_DATASET:

        query = item["query"]
        relevant_ids = item["relevant_ids"]

        query_embedding = embed(query)

        candidates = semantic_search(
            user_id=USER_ID,
            embedding=query_embedding,
            limit=VECTOR_SEARCH_K,
        )

        reranked = rerank(
            query,
            candidates,
        )

        results.append(
            {
                "query": query,
                "relevant_ids": relevant_ids,
                "reranked": reranked,
            }
        )

    return results


def evaluate(
    evaluation_results,
    threshold: float,
    limit: int,
):

    precision_scores = []
    recall_scores = []
    f1_scores = []
    ndcg_scores = []

    no_relevant_queries = 0
    false_positive_queries = 0

    memory_counts = []

    for item in evaluation_results:

        relevant_ids = item["relevant_ids"]

        filtered = [
            result for result in item["reranked"] if result["score"] >= threshold
        ]

        filtered = filtered[:limit]

        retrieved_ids = [result["id"] for result in filtered]

        memory_counts.append(len(retrieved_ids))

        if not relevant_ids:

            no_relevant_queries += 1

            if retrieved_ids:
                false_positive_queries += 1

            continue

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

        precision_scores.append(precision)

        recall_scores.append(recall)

        f1_scores.append(f1)

        ndcg_scores.append(ndcg)

    return {
        "threshold": threshold,
        "precision": mean(precision_scores),
        "recall": mean(recall_scores),
        "f1": mean(f1_scores),
        "ndcg": mean(ndcg_scores),
        "avg_memories": mean(memory_counts),
        "false_positive_rate": (
            false_positive_queries / no_relevant_queries if no_relevant_queries else 0.0
        ),
    }


def main():

    print("Preparing evaluation...")

    evaluation_results = prepare_evaluation()

    print(f"Queries: " f"{len(evaluation_results)}")

    for limit in RERANK_LIMITS:

        print("\n")
        print("=" * 100)
        print(f"RERANK LIMIT = {limit}")
        print("=" * 100)

        print(
            f"{'Threshold':>10}"
            f"{'Precision':>12}"
            f"{'Recall':>12}"
            f"{'F1':>12}"
            f"{'NDCG':>12}"
            f"{'AvgMem':>12}"
            f"{'FP Rate':>12}"
        )

        print("-" * 100)

        all_results = []

        for threshold in THRESHOLDS:

            result = evaluate(
                evaluation_results,
                threshold,
                limit,
            )

            all_results.append(result)

            print(
                f"{threshold:10.2f}"
                f"{result['precision']:12.3f}"
                f"{result['recall']:12.3f}"
                f"{result['f1']:12.3f}"
                f"{result['ndcg']:12.3f}"
                f"{result['avg_memories']:12.2f}"
                f"{result['false_positive_rate']:12.3f}"
            )

        # ---------------------------------------------
        # Best by F1
        # ---------------------------------------------

        best = max(
            all_results,
            key=lambda x: x["f1"],
        )

        print("\nBest by F1:")

        print(best)


if __name__ == "__main__":
    main()
