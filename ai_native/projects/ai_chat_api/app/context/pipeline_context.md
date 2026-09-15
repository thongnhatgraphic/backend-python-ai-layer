     User Query
                               │
                               ▼
                       Context Planner
                               │
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
            Memory            RAG           History
           required?        required?       required?
           priority         priority        priority
               │               │               │
               ▼               ▼               ▼
           Retrieve         Retrieve        Existing
           Memory            RAG             History
               │               │               │
               │          Reranker             │
               │               ↓               │
               │          Relevance Gate       │
               │               │               │
               └───────────────┼───────────────┘
                               ▼
                       Context Candidates
                               │
                               ▼
                       ContextAllocator
                               │
                               ▼
                        ContextBuilder
                               │
                               ▼
                              LLM