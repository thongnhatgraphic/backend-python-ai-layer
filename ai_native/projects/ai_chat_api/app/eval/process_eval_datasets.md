Bước 1 — Chuẩn bị Evaluation Dataset
    Xác định:
    Corpus documents.
    Evaluation queries.
    Ground-truth relevance (qrels).
    Số query thực sự dùng để đánh giá.

Ví dụ:
    Corpus     = 5,183 documents
    Queries    = 300 evaluation queries
    Qrels      = ground-truth relevant documents

Tạo file: 
    Ví dụ dataset_profile.md
        corpus size
        query count
        qrels count
        relevant docs/query
        score distribution
--------------------------------------------------

Bước 2 — Build Retrieval Metric
Xây metric cơ bản:
    Đánh giá các K:
    K = 5
    K = 10
    K = 20
    K = 50
    K = 100

=> Dense Retrieval Baseline
    Recall@5
    Recall@10
    Recall@20
    Recall@50
    Recall@100

Ví dụ: 
    Recall@5    = 75.34%
    Recall@10   = ...
    Recall@20   = 89.03%
    Recall@50   = ...
    Recall@100  = ...

--------------------------------------------------

Bước 3 — Benchmark Exact Dense Retrieval
Đo:
    Recall@K
    Latency
    P50
    P95
Tạo dense_exact_baseline.md

--------------------------------------------------

Bước 4 — Introduce HNSW
Thêm HNSW để chuyển:
    CREATE INDEX document_embedding_idx 
    ON document_embedding 
    USING hnsw (embedding vector_cosine_ops);

Exact Search
→ Approximate Nearest Neighbor Search

Sau đó benchmark:

ef_search = 10
            20
            40
            80
            100
            ...

Mỗi cấu hình ghi:
    Recall@20
    Latency P50
    Latency P95

Ví dụ vì trade-off phù hợp.

Chọn:
    K = 20
    ef_search = 40

Lưu hnsw_experiments.md

--------------------------------------------------

Bước 5 — Build Lexical Retrieval

PostgreSQL FTS

Đánh giá:
    Lexical Recall@20

Kiểm tra thêm:
    Dense MISS + Lexical HIT
    Dense HIT  + Lexical HIT
    Dense HIT  + Lexical MISS
    Dense MISS + Lexical MISS

Mục tiêu:
    Lexical có bổ sung tín hiệu cho Dense không?

Bước 6 — Quyết định Hybrid
Nếu có:
    Dense MISS
    +
    Lexical HIT

đáng kể → thử Hybrid/RRF.


Nếu:

Dense MISS + Lexical HIT ≈ 0
→ không thêm complexity chỉ vì Hybrid phổ biến.

Nếu khả thi thì mới hybrid_decision.md

--------------------------------------------------

Bước 7 — Đánh giá Reranker

Pipeline:
        Dense Top-K
            ↓
        Reranker
            ↓
        Top-N

Đo:
    Dense Recall@N
    Reranked Recall@N
    Improvement

Ví dụ:
    Dense Recall@5
    Reranked Recall@5
    Improvement = Reranked - Dense 

--------------------------------------------------

Bước 8 — Phân tích Reranker

Đếm:
    Rescued:
        Dense MISS → Reranker HIT

    Regression:
        Dense HIT → Reranker MISS

Từ đó biết:
    Reranker cứu được bao nhiêu?
    Reranker làm mất bao nhiêu?

Ví dụ Ettin:
    Rescued    = 19
    Regression = 6
    Net        = +13 query

Đây là diagnostic ( Chuẩn đoán ) quan trọng.

--------------------------------------------------

Bước 9 — Model Selection
Không chọn model chỉ dựa vào Recall.

Với mỗi candidate Model ghi:
    Model
    License
    Language
    Model size
    Recall@N
    Improvement
    Rescued
    Regression

Sau đó benchmark performance:
    P50
    P95
    Mean latency
    Latency/pair

--------------------------------------------------

Bước 10 — Chọn Operating Point

Cuối cùng chọn:
    Retriever K
    HNSW ef_search
    Reranker model
    Reranker candidate pool
    Final N

dựa trên:
    Quality
    Latency
    Resource
    Cost
    Deployment constraint

Ví dụ của chúng ta hiện tại:
    Dense:
    HNSW
    ef_search = 40
    K = 20

    Reranker:
    Ettin 150M
    N = 5

--------------------------------------------------

Bước 11 — Ghi lại Model Decision
Mà ghi:

Why selected:
- Recall@5
- improvement over dense
- rescued/regression
- latency
- model size
- license
- deployment feasibility



-------------------------------------------------------

Ở Bước 7 - 8 - 9

Đến đây ta đã có K từ quá trình tuning Retriever.

Ví dụ:
    K = 20

Bây giờ chọn một số:
    N = 5
    N = 10
    N = 15

Ví dụ K=20:

N < K
Dense Top-20
     │
     ├── Dense Top-5
     ├── Dense Top-10
     └── Dense Top-15


và đồng thời:
Dense Top-20
        ↓
Reranker
        ↓
        ├── Reranked Top-5
        ├── Reranked Top-10
        └── Reranked Top-15

Sau đó:

N = 5
    Dense Recall@5
    vs
    Reranked Recall@5

N = 10
    Dense Recall@10
    vs
    Reranked Recall@10

N = 15
    Dense Recall@15
    vs
    Reranked Recall@15


Bước 8:
    Dense Recall@5       = 75%
    Reranked Recall@5    = 80%

    Rescued              = 19
    Regression           = 6
    ============================
    Net improvement
    ≈ rescued - regression

Bước 9 — Test nhiều Reranker
Ví dụ:

Candidate Model A
Candidate Model B
Candidate Model C

Mỗi model phải đi qua cùng một protocol:
    Same dataset
    Same queries
    Same qrels
    Same Dense Retriever
    Same K
    Same N
    Same metric
    Same latency benchmark


Tóm lại:

Process chuẩn của bạn có thể ghi lại cực gọn như sau
1. Chọn tạm 1 Reranker để pipeline chạy.
2. Tune Dense Retriever → chốt K.
3. Với K đã chốt, chọn một số N < K.
4. Với từng N:
   Dense Top-N
   vs
   Dense Top-K → Reranker → Top-N
5. Đo Recall@N + Improvement.
6. Đo Rescue / Regression.
7. Lặp lại với các Reranker candidate khác.
8. So sánh Quality + Latency + Resource + Language + License.
9. Chọn model + K + N phù hợp production.