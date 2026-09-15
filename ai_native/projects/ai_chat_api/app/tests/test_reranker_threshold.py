from uuid import UUID

from FlagEmbedding import FlagReranker

from app.tests.test_semantic_search import semantic_search, embedding1, embedding2

USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")

VECTOR_SEARCH_K = 15
RERANKER_LIMIT = 5

THRESHOLDS = [
    0.00,
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
]


reranker = FlagReranker(
    "BAAI/bge-reranker-v2-m3",
    use_fp16=True,
)


def precision_at_k(
    retrieved_ids: set[str],
    relevant_ids: set[str],
) -> float:
    if not retrieved_ids:
        return 0.0

    hits = retrieved_ids & relevant_ids

    return len(hits) / len(retrieved_ids)


def recall_at_k(
    retrieved_ids: set[str],
    relevant_ids: set[str],
) -> float:
    if not relevant_ids:
        return 0.0

    hits = retrieved_ids & relevant_ids

    return len(hits) / len(relevant_ids)


def f1_score(
    precision: float,
    recall: float,
) -> float:
    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def rerank_candidates(
    query: str,
    candidates,
):
    pairs = [[query, candidate.memory.content] for candidate in candidates]

    scores = reranker.compute_score(
        pairs,
        normalize=True,
    )

    results = []

    for candidate, score in zip(candidates, scores):
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


def evaluate_threshold(
    reranked_candidates,
    relevant_ids: set[str],
    threshold: float,
    limit: int,
):
    filtered = [
        candidate
        for candidate in reranked_candidates
        if candidate["score"] >= threshold
    ]

    retrieved = filtered[:limit]

    retrieved_ids = {candidate["id"] for candidate in retrieved}

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

    return {
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "num_memories": len(retrieved),
    }


def run_experiment(
    experiment_name: str,
    query: str,
    embedding: list[float],
    relevant_ids: set[str],
):
    print("\n")
    print("=" * 80)
    print(experiment_name)
    print("=" * 80)

    # ---------------------------------------------------------
    # 1. Vector Search
    # ---------------------------------------------------------

    candidates = semantic_search(
        USER_ID,
        embedding,
        limit=VECTOR_SEARCH_K,
    )

    print(f"Vector Search candidates: {len(candidates)}")

    # ---------------------------------------------------------
    # 2. Reranker
    # ---------------------------------------------------------
    #
    # IMPORTANT:
    # Reranker chỉ chạy MỘT lần.
    # Sau đó chúng ta reuse scores cho mọi threshold.
    #

    reranked_candidates = rerank_candidates(
        query,
        candidates,
    )

    print("\nReranker ranking:")

    for rank, candidate in enumerate(
        reranked_candidates,
        start=1,
    ):
        print(f"{rank:2}. " f"{candidate['score']:.6f} " f"{candidate['content']}")

    # ---------------------------------------------------------
    # 3. Threshold experiment
    # ---------------------------------------------------------

    print("\n")
    print(
        f"{'Threshold':>10} "
        f"{'Precision':>10} "
        f"{'Recall':>10} "
        f"{'F1':>10} "
        f"{'Memories':>10}"
    )

    print("-" * 60)

    for threshold in THRESHOLDS:

        result = evaluate_threshold(
            reranked_candidates=reranked_candidates,
            relevant_ids=relevant_ids,
            threshold=threshold,
            limit=RERANKER_LIMIT,
        )

        print(
            f"{result['threshold']:10.2f} "
            f"{result['precision']:10.3f} "
            f"{result['recall']:10.3f} "
            f"{result['f1']:10.3f} "
            f"{result['num_memories']:10d}"
        )


def main():

    # =========================================================
    # Experiment 1
    # =========================================================

    experiment_1_relevant_ids = {
        "6b020aa3-7465-428b-b5cd-c8f90ce1b0e0",
        "adbbd8aa-d3e4-4911-9381-b469ccebca8e",
        "6f96724f-89f9-4865-9512-308253de116a",
        "a9022fdc-ca1d-4fa2-abef-861c9178a78c",
        "c02e1595-b121-4c73-8600-18e2aa3248c3",
    }

    run_experiment(
        experiment_name="Experiment 1: Tôi đang học Python",
        query="Tôi đang học Python",
        embedding=embedding1,
        relevant_ids=experiment_1_relevant_ids,
    )

    # =========================================================
    # Experiment 2
    # =========================================================

    experiment_2_relevant_ids = {
        "6b020aa3-7465-428b-b5cd-c8f90ce1b0e0",
        "adbbd8aa-d3e4-4911-9381-b469ccebca8e",
        "6f96724f-89f9-4865-9512-308253de116a",
        "a9022fdc-ca1d-4fa2-abef-861c9178a78c",
        "c02e1595-b121-4c73-8600-18e2aa3248c3",
    }

    run_experiment(
        experiment_name=("Experiment 2: " "Python là ngôn ngữ tôi đang tập trung học"),
        query="Python là ngôn ngữ tôi đang tập trung học",
        embedding=embedding2,
        relevant_ids=experiment_2_relevant_ids,
    )


if __name__ == "__main__":
    main()
