from app.services.reranker_service import RerankerService
from app.tests.test_semantic_search import (
    semantic_search,
    embedding1,
)
from app.tests.test_retrieval_evaluation import precision_at_k, recall_at_k
from uuid import UUID
from FlagEmbedding import FlagReranker

reranker_service = RerankerService(
    FlagReranker("BAAI/bge-reranker-v2-m3", use_fp16=True)
)

relevant_ids = {
    "6b020aa3-7465-428b-b5cd-c8f90ce1b0e0",
    "adbbd8aa-d3e4-4911-9381-b469ccebca8e",
    "6f96724f-89f9-4865-9512-308253de116a",
    "a9022fdc-ca1d-4fa2-abef-861c9178a78c",
    "c02e1595-b121-4c73-8600-18e2aa3248c3",
}
experiment1 = "Tôi đang học Python"
experiment2 = "Python là ngôn ngữ tôi đang tập trung học"
experiment3 = "Tôi muốn mua một chiếc xe"

for k in [5, 10, 15, 19]:

    candidates = semantic_search(
        UUID("43371a56-0d6b-454a-87c9-5c78b593122b"),
        embedding1,
        limit=k,
    )

    candidate_ids = {str(result.memory.id) for result in candidates}

    candidate_recall = recall_at_k(
        candidate_ids,
        relevant_ids,
    )

    reranked = reranker_service.rerank(
        query=experiment1,
        memories=candidates,
        limit=5,
    )

    reranked_ids = {str(result.memory.id) for result in reranked}

    precision = precision_at_k(
        reranked_ids,
        relevant_ids,
    )

    recall = recall_at_k(
        reranked_ids,
        relevant_ids,
    )

    print(
        f"K={k}",
        f"Candidate Recall={candidate_recall}",
        f"Reranker Precision@5={precision}",
        f"Reranker Recall@5={recall}",
    )
