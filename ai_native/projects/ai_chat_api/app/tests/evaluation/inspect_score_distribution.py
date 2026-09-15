import torch
from uuid import UUID
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


def rerank(query: str, candidates):
    pairs = [[query, candidate.memory.content] for candidate in candidates]

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

    return sorted(
        [
            {
                "id": str(candidate.memory.id),
                "content": candidate.memory.content,
                "score": score,
                "relevant": (str(candidate.memory.id) in current_relevant_ids),
            }
            for candidate, score in zip(
                candidates,
                scores,
            )
        ],
        key=lambda x: x["score"],
        reverse=True,
    )


def main():

    print("=" * 100)
    print("RELEVANT vs IRRELEVANT SCORE DISTRIBUTION")
    print("=" * 100)

    for item in EVALUATION_DATASET:

        if not item["relevant_ids"]:
            continue

        query = item["query"]

        global current_relevant_ids
        current_relevant_ids = item["relevant_ids"]

        embedding = embed(query)

        candidates = semantic_search(
            USER_ID,
            embedding,
            limit=VECTOR_SEARCH_K,
        )

        results = rerank(
            query,
            candidates,
        )

        relevant_scores = [result["score"] for result in results if result["relevant"]]

        irrelevant_scores = [
            result["score"] for result in results if not result["relevant"]
        ]

        print("\n")
        print("=" * 100)
        print(query)
        print("=" * 100)

        print(f"Highest relevant: " f"{max(relevant_scores):.6f}")

        print(f"Lowest relevant:  " f"{min(relevant_scores):.6f}")

        if irrelevant_scores:
            print(f"Highest irrelevant: " f"{max(irrelevant_scores):.6f}")

            print(f"Lowest irrelevant:  " f"{min(irrelevant_scores):.6f}")

        print("\nTop 10:")

        for rank, result in enumerate(
            results[:10],
            start=1,
        ):
            label = "RELEVANT" if result["relevant"] else "IRRELEVANT"

            print(
                f"{rank:2}. "
                f"{result['score']:9.4f} "
                f"{label:10} "
                f"{result['content']}"
            )


if __name__ == "__main__":
    main()
