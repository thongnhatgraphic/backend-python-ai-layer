def recall_at_k(retrieved_ids: list[str], relevent_ids: set[str], k: int) -> float:
    if not relevent_ids:
        return 0
    top_k = retrieved_ids[:k]

    result = set(top_k) & set(relevent_ids)
    return len(result) / len(relevent_ids)
