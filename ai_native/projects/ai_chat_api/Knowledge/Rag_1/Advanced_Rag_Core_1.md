1. Retrieval
    Embedding
    Vector Search
    HNSW
    ANN
    K
    Recall@K

2. Reranking
    Bi-encoder
    Cross-encoder
    Retriever → Reranker
    K → N
    Reranker quality
    Latency
    CPU feasibility

3. Hybrid Search
    Dense Search
    +
    BM25 / Lexical Search
    +
    Fusion

4. Context Engineering
Học ở mức thực dụng:
    Context selection                       
                                        user_message
                                            │
                                            ▼
                                        ContextPlanner
                                            │
                                        ContextPlan
                                            │
                            ┌────────────────┼────────────────┐
                            ▼                ▼                ▼
                        Memory             RAG            History
                        decision          decision         decision
                            │                │                │
                            │           required?            │
                            │                │               │
                            │              YES               │
                            │                ↓               │
                            │         Retrieve/Rerank        │
                            │                ↓               │
                            │              Gate              │
                            │                ↓               │
                            └────────────────┼───────────────┘
                                             ▼
                                        Context Candidates
                                             ↓
                                        ContextAllocator
                                             ↓
                                        ContextBuilder
    Deduplication
    Token budget
                                      Global Budget
                                            │
                                            ▼
                                    ContextAllocator
                                            │
                                    allocation budgets
                                ┌───────────┼───────────┐
                                ▼           ▼           ▼
                                Memory        RAG        History
                                2000         7000         1000
                                │           │             │
                                └───────────┼─────────────┘
                                            ▼
                                        ContextBuilder
                                            │
                                        fit actual items
                                            ▼
                                        final context
    Ordering
    Compression

5. RAG Evaluation
Bắt buộc.
    Recall@K
    Precision@K
    MRR / NDCG
    Reranker evaluation
    Answer relevance
    Groundedness
    Latency
    Cost