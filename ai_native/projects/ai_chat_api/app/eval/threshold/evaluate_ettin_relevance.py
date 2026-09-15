from pathlib import Path

from sqlmodel import Session

from app.eval.datasets.scifact.qrels_loader import load_qrels
from app.eval.datasets.scifact.query_loader import load_queries
from app.eval.metrics.retrieval_metrics import recall_at_k
from app.eval.retrieval.scifact_retriever import (
    engine,
    embedding_service,
    search_by_embedding,
)

from app.eval.reranking.ettin_reranker import EttinReranker

BASE_DIR = Path(__file__).resolve().parents[1] / "datasets" / "scifact"

QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"

RETRIEVAL_K = 20
FINAL_K = 5
EF_SEACRCH = 40
EVALUATION_QUERIES = 100


def evaluate():
    print("1. start evaluate")

    queries = load_queries(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    print("2. dataset loaded")

    evaluation_query_ids = sorted(list(qrels.keys()))[:EVALUATION_QUERIES]

    print("3. query ids:", len(evaluation_query_ids))

    print("4. loading reranker...")
    reranker = EttinReranker()
    print("5. reranker loaded")

    with Session(engine) as session:
        rows = []

        for query_id in evaluation_query_ids:
            query = queries[query_id]

            query_embedding = embedding_service.embed_text(query)

            results = search_by_embedding(
                session=session,
                query_embedding=query_embedding,
                limit=RETRIEVAL_K,
                ef_search=EF_SEACRCH,
            )

            reranked = reranker.rerank(
                query=query,
                results=results,
            )

            final_results = reranked[:FINAL_K]

            relevant_docs = qrels.get(query_id, set())

            for result in final_results:
                rows.append(
                    {
                        "query_id": query_id,
                        "doc_id": result.external_id,
                        "score": result.score,
                        "relevant": result.external_id in relevant_docs,
                    }
                )

        print("total rows:", len(rows))

        thresholds = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        print("\n===== THRESHOLD EVALUATION =====")

        total_relevant = sum(1 for row in rows if row["relevant"])

        for threshold in thresholds:
            passed = [row for row in rows if row["score"] >= threshold]

            relevant_kept = sum(1 for row in passed if row["relevant"])

            non_relevant_kept = sum(1 for row in passed if not row["relevant"])

            relevant_recall = (
                relevant_kept / total_relevant if total_relevant > 0 else 0.0
            )

            passed_count = len(passed)

            precision = relevant_kept / passed_count if passed_count > 0 else 0.0

            print(
                f"threshold={threshold:>2} | "
                f"relevant_kept={relevant_kept:>4} | "
                f"non_relevant_kept={non_relevant_kept:>4} | "
                f"recall={relevant_recall:.4f} | "
                f"precision={precision:.4f}"
            )


if __name__ == "__main__":
    evaluate()


# ===== THRESHOLD EVALUATION =====
# threshold= 0 | relevant_kept=  89 | non_relevant_kept= 410 | recall=1.0000 | precision=0.1784
# threshold= 1 | relevant_kept=  89 | non_relevant_kept= 406 | recall=1.0000 | precision=0.1798
# threshold= 2 | relevant_kept=  89 | non_relevant_kept= 373 | recall=1.0000 | precision=0.1926
# threshold= 3 | relevant_kept=  86 | non_relevant_kept= 326 | recall=0.9663 | precision=0.2087
# threshold= 4 | relevant_kept=  84 | non_relevant_kept= 248 | recall=0.9438 | precision=0.2530
# threshold= 5 | relevant_kept=  78 | non_relevant_kept= 155 | recall=0.8764 | precision=0.3348
# threshold= 6 | relevant_kept=  76 | non_relevant_kept=  98 | recall=0.8539 | precision=0.4368
# threshold= 7 | relevant_kept=  60 | non_relevant_kept=  63 | recall=0.6742 | precision=0.4878
# threshold= 8 | relevant_kept=  53 | non_relevant_kept=  28 | recall=0.5955 | precision=0.6543

# Đi tiếp vào context builder => thì pipeline sẽ là
# User Query
#     ↓
# Dense HNSW
# K = 20
# ef = 40
#     ↓
# Ettin
#     ↓
# Top 5
# N = 5
#     ↓
# Relevance Gate
# score >= 6
#     ↓
# 0..5 documents
#     ↓
# ContextBuilder
#     ↓
# Global Context Budget
#     ↓
# LLM
