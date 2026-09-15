RAG → Vector Retrieval → ANN → Performance Evaluation

| Parameter         | Khi nào? | Tác động chính              |
| ----------------- | -------- | --------------------------- |
| `m`               | Build    | Graph connectivity / memory |
| `ef_construction` | Build    | Graph quality / build time  |
| `ef_search`       | Query    | Recall / query latency      |


m
→ graph như thế nào?

ef_construction
→ xây graph kỹ đến mức nào?

ef_search
→ lúc query tôi tìm rộng đến mức nào?

Tạo HNSW index

Ta có:
    embedding <=> query_embedding => đây là cosine distance.

HNSW index phải dùng:
-----------------------------------------------------
    CREATE INDEX rag_documents_embedding_hnsw_idx
    ON rag_documents
    USING hnsw (embedding vector_cosine_ops);
-----------------------------------------------------

    Để xoá Index
-----------------------------------------------------
    DROP INDEX CONCURRENTLY rag_documents_embedding_hnsw_idx;
-----------------------------------------------------

    ef_search có thể set trong transaction
    """
        BEGIN;

        SET LOCAL hnsw.ef_search = 80;

        SELECT
            external_id,
            1 - (embedding <=> :query_embedding) AS score
        FROM rag_documents
        ORDER BY embedding <=> :query_embedding
        LIMIT 20;

        COMMIT;
    """


                    HNSW
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     ef_search=10  ef=40      ef=100
          │           │           │
          ▼           ▼           ▼
       Recall       Recall      Recall
          │           │           │
          ▼           ▼           ▼
       Latency      Latency     Latency


ef_search
→ HNSW search nội bộ rộng đến mức nào?

HNSW sinh ra để giúp nearest-neighbor search ở quy mô lớn, nhưng với dataset nhỏ, exact scan có thể đã đủ nhanh.

Evaluation =>

    Exact Search
        ↓
    Baseline
        │
        ├── Recall@K
        └── Latency
            ↓
            HNSW
            ↓
        Recall@K + Latency
            ↓
        Compare