import os
import time
from uuid import UUID

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.tests.test_semantic_search import semantic_search, embedding1

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

USER_ID = UUID("43371a56-0d6b-454a-87c9-5c78b593122b")

QUERY = "Tôi đang học Python"

K = 15

NUM_THREADS = 12


def benchmark_model(
    model,
    inputs,
    runs: int = 20,
) -> float:
    """
    Benchmark model inference latency.

    Tokenization is NOT included.
    """

    model.eval()

    # Warm-up
    with torch.no_grad():
        model(
            **inputs,
            return_dict=True,
        )

    times = []

    for _ in range(runs):
        start = time.perf_counter()

        with torch.no_grad():
            model(
                **inputs,
                return_dict=True,
            )

        elapsed = time.perf_counter() - start

        times.append(elapsed * 1000)

    average = sum(times) / len(times)

    return average


def get_scores(model, inputs) -> list[float]:
    """
    Run inference and return reranker scores.
    """

    model.eval()

    with torch.no_grad():
        scores = (
            model(
                **inputs,
                return_dict=True,
            )
            .logits.view(-1)
            .float()
        )

    return scores.tolist()


def print_ranking(
    pairs: list[list[str]],
    scores: list[float],
    title: str,
) -> list[str]:
    """
    Sort memories by reranker score descending
    and print Top 5.
    """

    results = sorted(
        zip(pairs, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    print(f"\n===== {title} =====")

    top_ids = []

    for rank, (pair, score) in enumerate(results[:5], start=1):
        print(f"Rank {rank}: " f"{score:.6f} | " f"{pair[1]}")

    return top_ids


def main():
    # ---------------------------------------------------------
    # 1. CPU configuration
    # ---------------------------------------------------------

    torch.set_num_threads(NUM_THREADS)

    print("CPU cores:", os.cpu_count())
    print("PyTorch threads:", torch.get_num_threads())

    # ---------------------------------------------------------
    # 2. Load candidates
    # ---------------------------------------------------------

    candidates = semantic_search(
        USER_ID,
        embedding1,
        limit=19,
    )

    pairs = [[QUERY, memory.memory.content] for memory in candidates[:K]]

    print("Number of candidates:", len(pairs))

    # ---------------------------------------------------------
    # 3. Tokenizer
    # ---------------------------------------------------------

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512,
    )

    # ---------------------------------------------------------
    # 4. Load FP32 model
    # ---------------------------------------------------------

    print("\nLoading FP32 model...")

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    model.eval()

    # ---------------------------------------------------------
    # 5. Benchmark FP32
    # ---------------------------------------------------------

    fp32_latency = benchmark_model(
        model,
        inputs,
    )

    fp32_scores = get_scores(
        model,
        inputs,
    )

    print(f"\nFP32 latency: {fp32_latency:.2f} ms")

    print_ranking(
        pairs,
        fp32_scores,
        "FP32 Top 5",
    )

    # ---------------------------------------------------------
    # 6. Quantization
    # ---------------------------------------------------------

    print("\nQuantizing model to INT8...")

    # API mới của PyTorch / torchao
    from torchao.quantization import (
        quantize_,
        Int8WeightOnlyConfig,
    )

    int8_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    int8_model.eval()

    quantize_(
        int8_model,
        Int8WeightOnlyConfig(),
    )

    # ---------------------------------------------------------
    # 7. Benchmark INT8
    # ---------------------------------------------------------

    int8_latency = benchmark_model(
        int8_model,
        inputs,
    )

    int8_scores = get_scores(
        int8_model,
        inputs,
    )

    print(f"\nINT8 latency: {int8_latency:.2f} ms")

    print_ranking(
        pairs,
        int8_scores,
        "INT8 Top 5",
    )

    # ---------------------------------------------------------
    # 8. Summary
    # ---------------------------------------------------------

    print("\n==============================")
    print("SUMMARY")
    print("==============================")

    print(f"FP32 latency: {fp32_latency:.2f} ms")

    print(f"INT8 latency: {int8_latency:.2f} ms")

    speedup = fp32_latency / int8_latency

    print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    main()
