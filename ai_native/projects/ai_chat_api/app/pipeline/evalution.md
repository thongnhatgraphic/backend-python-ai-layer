                 Production
                     │
                     ▼
               Query Logs
                     │
                     ▼
              Sample Queries
                     │
                     ▼
             Candidate Pooling
              /       |       \
             /        |        \
       Vector       BM25      Hybrid
             \        |        /
              \       |       /
               ▼      ▼      ▼
              Candidate Set
                     │
                     ▼
              LLM Annotation
                     │
                     ▼
               Human Review
                     │
                     ▼
             Evaluation Dataset
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Recall@K     Precision@K    NDCG@K


    -------------------------------------------
Database:
19
10,000
1,000,000
100,000,000

evaluation framework:
Evaluation Queries
        ↓
Retriever
        ↓
Top K
        ↓
Ground Truth
        ↓
Metrics

---------------------------------
Với database nhỏ thì
19 records hiện tại đang rất tốt để học:
Ground Truth
↓
Top-K
↓
Precision
↓
Recall
↓
K trade-off
-------------------------------------
Sau khi hiểu chắc phần này, chúng ta sẽ nâng lên:
Evaluation Dataset
↓
LLM-assisted annotation
↓
NDCG@K
↓
Threshold calibration
↓
Reranker evaluation