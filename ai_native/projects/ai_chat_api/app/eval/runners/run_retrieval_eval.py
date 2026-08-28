def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    top_k = retrieved_ids[:k]

    if not relevant_ids:
        return 0.0

    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)

    return hits / len(relevant_ids)
