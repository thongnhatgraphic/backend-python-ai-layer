from uuid import UUID

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

from app.tests.evaluation.reranker_eval_dataset import (
    EVALUATION_DATASET,
)
from app.tests.test_semantic_search import (
    embed,
    semantic_search,
)

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")

VECTOR_SEARCH_K = 15


torch.set_num_threads(12)


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()


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


def main():

    print("=" * 90)
    print("NEGATIVE QUERY INSPECTION")
    print("=" * 90)

    for item in EVALUATION_DATASET:

        if item["relevant_ids"]:
            continue

        query = item["query"]

        print("\n")
        print("-" * 90)
        print(f"Query: {query}")
        print("-" * 90)

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

        print("\nTop 5 reranker results:")

        for rank, result in enumerate(
            reranked[:5],
            start=1,
        ):
            print(f"{rank}. " f"score={result['score']:.6f} | " f"{result['content']}")


if __name__ == "__main__":
    main()
