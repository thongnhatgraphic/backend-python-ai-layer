import math
import time
from statistics import mean, median
from uuid import UUID

import torch
from transformers import AutoModel, AutoModelForSequenceClassification
from transformers import AutoTokenizer

from app.tests.evaluation.reranker_eval_dataset import (
    EVALUATION_DATASET,
)
from app.tests.test_semantic_search import (
    embed,
    semantic_search,
)

# ============================================================
# Configuration
# ============================================================

USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")

VECTOR_SEARCH_K = 15
RERANK_TOP_K = 5

WARMUP_RUNS = 2

# Giữ giống experiment CPU trước của chúng ta
torch.set_num_threads(6)

print("PyTorch threads:", torch.get_num_threads())


# ============================================================
# BGE
# ============================================================

BGE_MODEL_NAME = "BAAI/bge-reranker-v2-m3"

print("\nLoading BGE...")

bge_tokenizer = AutoTokenizer.from_pretrained(
    BGE_MODEL_NAME,
)

bge_model = AutoModelForSequenceClassification.from_pretrained(
    BGE_MODEL_NAME,
)

bge_model.eval()


# ============================================================
# Jina
# ============================================================

JINA_MODEL_NAME = "jinaai/jina-reranker-v3"

print("\nLoading Jina...")

jina_model = AutoModel.from_pretrained(
    JINA_MODEL_NAME,
    dtype="auto",
    trust_remote_code=True,
)

jina_model.eval()


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

    ideal_relevant_count = min(
        len(relevant_ids),
        k,
    )

    idcg = 0.0

    for rank in range(
        1,
        ideal_relevant_count + 1,
    ):
        idcg += 1 / math.log2(rank + 1)

    if idcg == 0:
        return 0.0

    return dcg / idcg


# ============================================================
# BGE direct
# ============================================================


def rerank_bge(
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

    inputs = bge_tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512,
    )

    with torch.no_grad():

        scores = (
            bge_model(
                **inputs,
                return_dict=True,
            )
            .logits.view(-1)
            .float()
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
                "score": float(score),
            }
        )

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True,
    )


# ============================================================
# Jina
# ============================================================


def rerank_jina(
    query: str,
    candidates,
):
    documents = [candidate.memory.content for candidate in candidates]

    results = jina_model.rerank(
        query,
        documents,
        top_n=None,
    )

    reranked = []

    for result in results:

        index = result["index"]

        candidate = candidates[index]

        reranked.append(
            {
                "id": str(candidate.memory.id),
                "content": candidate.memory.content,
                "score": float(result["relevance_score"]),
            }
        )

    return reranked


# ============================================================
# Evaluate one query
# ============================================================


def evaluate_ranking(
    reranked,
    relevant_ids: set[str],
):
    top_results = reranked[:RERANK_TOP_K]

    retrieved_ids = [result["id"] for result in top_results]

    return {
        "precision": precision_at_k(
            retrieved_ids,
            relevant_ids,
        ),
        "recall": recall_at_k(
            retrieved_ids,
            relevant_ids,
        ),
        "ndcg": ndcg_at_k(
            retrieved_ids,
            relevant_ids,
            RERANK_TOP_K,
        ),
    }


# ============================================================
# Benchmark one model
# ============================================================


def benchmark_model(
    model_name: str,
    rerank_function,
    queries,
):
    print("\n")
    print("=" * 70)
    print(model_name)
    print("=" * 70)

    precision_scores = []
    recall_scores = []
    ndcg_scores = []

    latencies = []

    # --------------------------------------------------------
    # Warm-up
    # --------------------------------------------------------

    print("\nWarm-up...")

    warmup_query = queries[0]

    candidates = semantic_search(
        USER_ID,
        embed(warmup_query["query"]),
        limit=VECTOR_SEARCH_K,
    )

    for _ in range(WARMUP_RUNS):

        rerank_function(
            warmup_query["query"],
            candidates,
        )

    print("Warm-up completed.")

    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    for index, item in enumerate(
        queries,
        start=1,
    ):

        query = item["query"]
        relevant_ids = item["relevant_ids"]

        # ----------------------------------------------------
        # Candidate generation
        #
        # Retrieval is NOT included in reranker latency.
        # Both models receive exactly the same candidates.
        # ----------------------------------------------------

        query_embedding = embed(query)

        candidates = semantic_search(
            USER_ID,
            query_embedding,
            limit=VECTOR_SEARCH_K,
        )

        # ----------------------------------------------------
        # Reranker latency
        # ----------------------------------------------------

        start = time.perf_counter()

        reranked = rerank_function(
            query,
            candidates,
        )

        elapsed = (time.perf_counter() - start) * 1000

        latencies.append(elapsed)

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        metrics = evaluate_ranking(
            reranked,
            relevant_ids,
        )

        precision_scores.append(metrics["precision"])

        recall_scores.append(metrics["recall"])

        ndcg_scores.append(metrics["ndcg"])

        # ----------------------------------------------------
        # Print query result
        # ----------------------------------------------------

        print(f"\nQuery {index}: {query}")

        print(f"Latency: {elapsed:.2f} ms")

        print(f"Precision@{RERANK_TOP_K}: " f"{metrics['precision']:.3f}")

        print(f"Recall@{RERANK_TOP_K}: " f"{metrics['recall']:.3f}")

        print(f"NDCG@{RERANK_TOP_K}: " f"{metrics['ndcg']:.3f}")

        print("Top results:")

        for rank, result in enumerate(
            reranked[:RERANK_TOP_K],
            start=1,
        ):
            print(f"  {rank}. " f"{result['score']:.6f} " f"{result['content']}")

    # ========================================================
    # Aggregate
    # ========================================================

    sorted_latencies = sorted(latencies)

    p95_index = max(
        0,
        math.ceil(0.95 * len(sorted_latencies)) - 1,
    )

    p95 = sorted_latencies[p95_index]

    result = {
        "model": model_name,
        "precision": mean(precision_scores),
        "recall": mean(recall_scores),
        "ndcg": mean(ndcg_scores),
        "p50": median(latencies),
        "p95": p95,
        "mean_latency": mean(latencies),
    }

    print("\n")
    print("-" * 70)
    print(f"{model_name} SUMMARY")
    print("-" * 70)

    print(f"Precision@{RERANK_TOP_K}: " f"{result['precision']:.4f}")

    print(f"Recall@{RERANK_TOP_K}: " f"{result['recall']:.4f}")

    print(f"NDCG@{RERANK_TOP_K}: " f"{result['ndcg']:.4f}")

    print(f"Mean latency: " f"{result['mean_latency']:.2f} ms")

    print(f"P50 latency: " f"{result['p50']:.2f} ms")

    print(f"P95 latency: " f"{result['p95']:.2f} ms")

    return result


# ============================================================
# Main
# ============================================================


def main():

    print("\n")
    print("=" * 70)
    print("RERANKER MODEL EVALUATION")
    print("=" * 70)

    print(f"Dataset size: " f"{len(EVALUATION_DATASET)} queries")

    print(f"Vector Search K: " f"{VECTOR_SEARCH_K}")

    print(f"Reranker Top K: " f"{RERANK_TOP_K}")

    # --------------------------------------------------------
    # BGE
    # --------------------------------------------------------

    bge_result = benchmark_model(
        model_name="BGE-v2-m3 / Transformers",
        rerank_function=rerank_bge,
        queries=EVALUATION_DATASET,
    )

    # --------------------------------------------------------
    # Jina
    # --------------------------------------------------------

    jina_result = benchmark_model(
        model_name="Jina-reranker-v3",
        rerank_function=rerank_jina,
        queries=EVALUATION_DATASET,
    )

    # ========================================================
    # Final comparison
    # ========================================================

    print("\n")
    print("=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(f"{'Metric':<20}" f"{'BGE':>15}" f"{'Jina':>15}")

    print("-" * 50)

    print(
        f"{'Precision@5':<20}"
        f"{bge_result['precision']:>15.4f}"
        f"{jina_result['precision']:>15.4f}"
    )

    print(
        f"{'Recall@5':<20}"
        f"{bge_result['recall']:>15.4f}"
        f"{jina_result['recall']:>15.4f}"
    )

    print(
        f"{'NDCG@5':<20}" f"{bge_result['ndcg']:>15.4f}" f"{jina_result['ndcg']:>15.4f}"
    )

    print(
        f"{'Mean latency':<20}"
        f"{bge_result['mean_latency']:>15.2f}"
        f"{jina_result['mean_latency']:>15.2f}"
    )

    print(
        f"{'P50 latency':<20}"
        f"{bge_result['p50']:>15.2f}"
        f"{jina_result['p50']:>15.2f}"
    )

    print(
        f"{'P95 latency':<20}"
        f"{bge_result['p95']:>15.2f}"
        f"{jina_result['p95']:>15.2f}"
    )


if __name__ == "__main__":
    main()
