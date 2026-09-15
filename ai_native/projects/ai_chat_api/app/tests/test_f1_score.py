from app.tests.test_retrieval_evaluation import precision_at_k, recall_at_k
from app.schemas.memory_search_schema import MemorySearchResult
from app.tests.test_semantic_search import semantic_search1, semantic_search2


def f1_score(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)


def evaluate_threshold(
    results: list[MemorySearchResult],
    relevant_ids: set[str],
    threshold: float,
):
    filtered_ids = {
        str(result.memory.id) for result in results if result.score >= threshold
    }

    precision = precision_at_k(
        filtered_ids,
        relevant_ids,
    )

    recall = recall_at_k(
        filtered_ids,
        relevant_ids,
    )

    f1 = f1_score(precision, recall)

    return precision, recall, f1


thresholds = [
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
    0.75,
]

relevant_ids = {
    "6b020aa3-7465-428b-b5cd-c8f90ce1b0e0",
    "adbbd8aa-d3e4-4911-9381-b469ccebca8e",
    "6f96724f-89f9-4865-9512-308253de116a",
    "a9022fdc-ca1d-4fa2-abef-861c9178a78c",
    "c02e1595-b121-4c73-8600-18e2aa3248c3",
}

results_exp1 = semantic_search1
results_exp2 = semantic_search2

for threshold in thresholds:
    precision, recall, f1 = evaluate_threshold(
        results_exp1,
        relevant_ids,
        threshold,
    )

    print(
        threshold,
        precision,
        recall,
        f1,
    )

for threshold in thresholds:
    precision, recall, f1 = evaluate_threshold(
        results_exp2,
        relevant_ids,
        threshold,
    )

    print(
        threshold,
        precision,
        recall,
        f1,
    )

# DCG Discounted Cumulative Gain
# Tôi đang có ranking này. Nó mang lại bao nhiêu giá trị?

# IDCG
# Nếu tôi xếp ranking hoàn hảo thì tôi có thể đạt bao nhiêu giá trị?

# NDCG
# Ranking hiện tại của tôi đạt bao nhiêu phần trăm so với ranking hoàn hảo?

# Hay DCG
# = Ranking hiện tại tốt đến đâu?
# --------------------------------
# IDCG
# = Ranking hoàn hảo tốt đến đâu?
# ---------------------------------
# NDCG
# = Ranking hiện tại đạt bao nhiêu % của ranking hoàn hảo?

# NDCG = DCG / IDCG

# Ranking thực tế
# [3, 2, 0, 3, 3]
#  ↑
# Vector Search trả về

# Ranking lý tưởng
# [3, 3, 3, 2, 0]
#  ↑
# Nếu chúng ta xếp hoàn hảo

# Sau đó:
# DCG  = giá trị của [3,2,0,3,3]
# IDCG = giá trị của [3,3,3,2,0]

# Cuối cùng:
# NDCG = DCG / IDCG


#                 Retrieval Evaluation
#                        │
#          ┌─────────────┴─────────────┐
#          │                           │
#    Offline Evaluation          Online Evaluation
#          │                           │
#    Evaluation Set              Production Signals
#          │                           │
#  Precision / Recall             User feedback
#  NDCG / MRR                     Usage
#  Threshold                     Answer quality
