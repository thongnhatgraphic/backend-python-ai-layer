RAG Evaluation

    AI Engineer
    ↓
    RAG
    ↓
    Evaluation
    ↓
    Retrieval Evaluation
    ↓
    Generation Evaluation

    Trong project:

                        Query
                        ↓
                        Retriever
                        ↓
                        K
                        ↓
                        Reranker
                        ↓
                        N
                        ↓
                        Context
                        ↓
                        LLM

Evaluation phải trả lời từng câu hỏi:

    Retriever có tìm đúng không?
                => Did relevant docs enter candidate pool?
            ↓
    Reranker có rank đúng không?
                => Did relevant docs move toward the top?
            ↓
    Context có đủ tốt không?
            ↓
    LLM có trả lời đúng không?


1. Mean Reciprocal Rank
    Relevant result đầu tiên nằm ở vị trí bao nhiêu?
    Relevant document đầu tiên xuất hiện ở rank bao nhiêu?

    A = relevant
    Rank 1
    → score = 1/1 = 1.0

    Rank 2
    → score = 1/2 = 0.5

    Rank 5
    → score = 1/5 = 0.2
-----------------------------------------------
    Query 1 → first relevant at rank 1 → 1.0
    Query 2 → rank 2                → 0.5
    Query 3 → rank 4                → 0.25
-----------------------------------------------
    MRR = (1+0.5+0.25​) / 3

2. NDCG
    Không phải tất cả documents đều relevant ở cùng một mức độ.
    D1 = highly relevant
    D2 = relevant
    D3 = somewhat relevant
    D4 = irrelevant

    NDCG đánh giá:
    Ranking có đặt những documents có relevance cao lên phía trên không?


| Component       | Metric chính                        |
| --------------- | ----------------------------------- |
| Retriever       | Recall@K                            |
| Retriever       | Precision@K                         |
| Reranker        | MRR                                 |
| Reranker        | NDCG                                |
| Context         | Coverage / redundancy / token usage |
| LLM             | Answer quality / groundedness       |
| Entire pipeline | Latency / cost                      |


                     RAG
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     Retrieval     Ranking      Generation
        │             │             │
    Recall@K       MRR/NDCG       Answer
    Precision@K                     │
                                    ├─ Correctness
                                    ├─ Relevance
                                    └─ Groundedness


Một evaluation sample tối thiểu nên có:
    {
        "query": "...",
        "relevant_document_ids": [
            "...",
            "...",
        ]
    }

    Ví dụ:
    {
        "query": "Why does increasing ef_search improve recall?",
        "relevant_document_ids": [
            "doc_12",
            "doc_37",
            "doc_81",
        ]
    }
Retriever sẽ chạy:
    query
    ↓
    embedding
    ↓
    search
    ↓
    Top-K


    rồi evaluation code tính:
    Recall@5
    Recall@10
    Recall@20
    Recall@50



                    BEIR
                     │
       ┌─────────────┼─────────────┐
       │             │             │
   SciFact       HotpotQA      DBpedia
       │             │             │
       └─────────────┼─────────────┘
                     │
              Retrieval benchmark


SciFact HotpotQA DBpedia
→ Dataset

BEIR
→ Benchmark suite / evaluation framework

qrels
→ Ground truth relevance judgments

Recall@K / NDCG@K / MRR
→ Metrics

PostgreSQL + pgvector
→ Retrieval system under evaluation