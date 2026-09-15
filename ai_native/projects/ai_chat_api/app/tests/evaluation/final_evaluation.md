                    Evaluation Dataset
                           │
                 ┌─────────┴─────────┐
                 │                   │
               Query              Ground Truth
                 │                   │
                 └─────────┬─────────┘
                           ↓
                    Retrieval System
                           ↓
                    Vector Search
                           ↓
                         Top K
                           ↓
                       Reranker
                           ↓
                      Threshold
                           ↓
                        Top N
                           ↓
              ┌────────────┼────────────┐
              ↓            ↓            ↓
          Precision      Recall        F1



          Production data
            10,000 memories
                ↓
            Không label 10,000
                ↓
            Xây evaluation set
                ↓
            50–200 queries
                ↓
            Ground truth
                ↓
            Automated evaluation



Ta chỉ cần tìm threshold tạo ra trade-off tốt:

Precision ↑
Recall ↑
F1 ↑
NDCG ↑
False Positive ↓
Average memories ↓