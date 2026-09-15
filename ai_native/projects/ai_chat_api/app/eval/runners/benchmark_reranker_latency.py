import time
from pathlib import Path

from sqlmodel import Session

from app.eval.datasets.scifact.qrels_loader import load_qrels
from app.eval.datasets.scifact.query_loader import load_queries
from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)
from app.eval.reranking.bge_reranker import BGEReranker
from app.eval.reranking.ettin_reranker import EttinReranker

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"

RETRIEVAL_K = 20
NUM_QUERIES = 20
WARMUP_RUNS = 2


def percentile(values: list[float], p: float) -> float:
    return float(__import__("numpy").percentile(values, p))


def benchmark():

    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    query_ids = sorted(list(qrels.keys()))[:NUM_QUERIES]

    reranker = EttinReranker()

    # --------------------------------
    # Prepare Dense Top-20 candidates
    # --------------------------------

    query_candidates = []

    with Session(engine) as session:

        for query_id in query_ids:

            query_text = queries[query_id]

            query_embedding = embedding_service.embed_text(query_text)

            dense_results = search_by_embedding(
                session=session,
                query_embedding=query_embedding,
                limit=RETRIEVAL_K,
                ef_search=40,
            )

            query_candidates.append((query_text, dense_results))

    print(
        f"Prepared {len(query_candidates)} queries "
        f"with {RETRIEVAL_K} candidates each."
    )

    # --------------------------------
    # Warmup
    # --------------------------------

    for query_text, dense_results in query_candidates[:WARMUP_RUNS]:
        reranker.rerank(
            query=query_text,
            results=dense_results,
        )

    # --------------------------------
    # Benchmark
    # --------------------------------

    latencies_ms = []
    total_pairs = 0

    for query_text, dense_results in query_candidates:

        start = time.perf_counter()

        reranker.rerank(
            query=query_text,
            results=dense_results,
        )

        elapsed_ms = (time.perf_counter() - start) * 1000

        latencies_ms.append(elapsed_ms)

        total_pairs += len(dense_results)

    print()
    print("========================================")
    print("BGE Reranker Latency Benchmark")
    print("========================================")

    print("Queries:", len(query_candidates))
    print("Candidates/query:", RETRIEVAL_K)
    print("Total pairs:", total_pairs)

    print(f"P50 latency/query: " f"{percentile(latencies_ms, 50):.2f} ms")

    print(f"P95 latency/query: " f"{percentile(latencies_ms, 95):.2f} ms")

    print(f"Mean latency/query: " f"{sum(latencies_ms) / len(latencies_ms):.2f} ms")

    print(f"Approx latency/pair: " f"{sum(latencies_ms) / total_pairs:.2f} ms")


if __name__ == "__main__":
    benchmark()
