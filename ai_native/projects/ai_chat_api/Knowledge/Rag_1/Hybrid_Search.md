🔀 Hybrid Search

RAG → Retrieval → Hybrid Retrieval

"abnormal"
"PrP"
"positivity"
"UK"

                 Retrieval
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
      Dense                     Lexical
       │                           │
      HNSW                      FTS/BM25
       │                           │
       └─────────────┬─────────────┘
                     ▼
                   Hybrid
                     │
                    RRF
                     │
                     ▼
                  Reranker
                     │
                     ▼
                     N
                     │
                     ▼
                Context Builder