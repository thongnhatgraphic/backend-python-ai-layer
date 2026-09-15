PHẦN I — XÁC ĐỊNH BÀI TOÁN

Đừng bắt đầu bằng:
"Model reranker nào tốt?"

Bắt đầu bằng:
Task
Language
Quality requirement
Latency requirement
Hardware
Cost
License
Inference environment

Ví dụ project của chúng ta:

    Task:
    Reranking retrieved memories

    Language:
    Vietnamese + English

    Hardware:
    CPU

    Candidate:
    Top K memories

    Final context:
    Top N memories

    Requirement:
    quality tốt + CPU feasible

PHẦN II — SHORTLIST MODEL
1. Đúng task reranking?
2. Multilingual / Vietnamese?
3. Model size?
4. Benchmark?
5. CPU/GPU feasibility?
6. License?
7. Cách inference?
8. Community / maintenance?

Project của chúng ta:
    Candidate A:
    BAAI/bge-reranker-v2-m3

    Candidate B:
    jinaai/jina-reranker-v3

PHẦN III — XÂY EVALUATION DATASET

Không làm:
    10,000 memories
    ×
    manual inspection

Mà tạo một evaluation set nhỏ:
10 → 50 → 100 → 500 queries

Dataset của chúng ta có:
    Learning
    Identity
    Preference
    Hobby
    Career
    No-relevant-memory
Evaluation dataset phải đại diện cho các loại query thực tế, không chỉ một chủ đề.


PHẦN IV — CỐ ĐỊNH CANDIDATE POOL
Query
 ↓
Embedding
 ↓
Vector Search
 ↓
Top K

Quan trọng: BGE và Jina phải nhận cùng candidate set.


PHẦN V — CHỌN K

K = số candidate đưa vào Reranker.
K = 5
K = 10
K = 15
K = 19

|  K | Candidate Recall |
| -: | ---------------: |
|  5 |              0.6 |
| 10 |              0.8 |
| 15 |          **1.0** |
| 19 |          **1.0** |
Đồng thời latency tăng theo K.
    Từ đó:

    K=5
    → candidate chưa đủ

    K=10
    → tốt hơn nhưng vẫn mất relevant

    K=15
    → đủ

    K=19
    → không thêm quality

* - Nguyên tắc tổng quát
Chọn K nhỏ nhất nhưng candidate recall đã đạt mức business chấp nhận.

K ↑
→ recall ↑
→ reranker workload ↑
→ latency ↑
→ cost ↑

PHẦN VI — SO SÁNH MODEL
Sau khi có:
K = 15

chúng ta chạy:

BGE
Jina

trên cùng dataset + cùng candidates.

BGE:

Precision@5 = 0.4889
Recall@5    = 0.6481
NDCG@5      = 0.6811

P95 ≈ 867 ms

Jina:

Precision@5 = 0.4889
Recall@5    = 0.6481
NDCG@5      = 0.7019

P95 ≈ 9842 ms


PHẦN VII — PHÂN BIỆT MODEL VÀ INFERENCE STACK
Chúng ta có:

BGE-v2-m3
├── FlagEmbedding
│   └── ~1.4s
│
└── Transformers direct
    └── ~0.7–0.8s

    Đây là cùng model nhưng inference stack khác nhau.

PHẦN VIII — SAU KHI CHỌN MODEL MỚI CALIBRATE THRESHOLD

Đây là chỗ trước đó chúng ta đi hơi lệch thứ tự.

Đúng ra:
    ❌ Chọn threshold
    → rồi mới chọn model

    Model selection
        ↓
Chọn inference stack
        ↓
Threshold calibration


PHẦN IX — THRESHOLD CALIBRATION

Sau khi BGE direct được chốt:

    Vector Search
        ↓
    K=15
        ↓
    BGE direct

    ta thu score của toàn bộ evaluation dataset.


    ta thu score của toàn bộ evaluation dataset.

Sau đó thử:

threshold
0.00
0.01
0.02
...

Với mỗi threshold:

Precision
Recall
F1
Average memories returned


Mục tiêu
Không phải:
threshold có Precision cao nhất.
Mà là:
threshold thỏa business requirement.


PHẦN X — CHỌN FINAL LIMIT

    Sau Reranker:

    15 candidates
    ↓
    reranker
    ↓
    ?

    Ta cần quyết định N, tức số memory cuối cùng đưa vào Context.

    Ví dụ:

    N = 3
    N = 5
    N = 7
    N = 10

    Đánh giá:

    Recall
    Precision
    NDCG
    Context tokens
    LLM latency
    LLM cost


PHẦN XI — CHỌN K VÀ N KHÁC NHAU

        Đây là kiến trúc rất quan trọng:

        Database
        ↓
        Vector Search
        ↓
        K = 15
        ↓
        15 candidates
        ↓
        Reranker
        ↓
        N = 5
        ↓
        ContextBuilder


K
Candidate pool
Ưu tiên:
Recall

N
Final context
Ưu tiên:
Precision
Token budget
Cost
LLM quality

Không nên:
K = N = 5
một cách mặc định.

PHẦN XII — CẤU TRÚC DECISION CUỐI CÙNG
                ┌──────────────────────┐
                │   Business Problem   │
                └──────────┬───────────┘
                           ↓
                    Requirements
                           ↓
                  Candidate Models
                           ↓
                Evaluation Dataset
                           ↓
                  Choose Candidate K
                           ↓
               Same candidates for all
                           ↓
                    Model Benchmark
                           ↓
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       Quality          Latency           Cost
          │                │                │
          └────────────────┼────────────────┘
                           ↓
                    Choose Model
                           ↓
               Choose Inference Stack
                           ↓
                 Threshold Calibration
                           ↓
                    Choose Final N
                           ↓
                  Context Token Budget
                           ↓
                   Production Pipeline



PHẦN XIII — APPLY VÀO PROJECT CỦA CHÚNG TA
Embedding Model
    ↓
nomic-embed-text
    ↓
Vector Search
    ↓
Candidate K = 15      ← provisional
    ↓
BGE-v2-m3             ← chosen baseline/winner
    ↓
Transformers direct   ← inference stack
    ↓
Threshold = ???       ← chưa calibrate
    ↓
Top N = 5             ← provisional
    ↓
ContextBuilder


PHẦN XIV — QUY TRÌNH CHO BẤT KỲ PROJECT MỚI
1. Define task
2. Define constraints
3. Shortlist 2–4 models
4. Build evaluation dataset
5. Fix candidate K
6. Run all models on same candidates
7. Measure quality
8. Measure latency
9. Check license/cost/resource
10. Choose model
11. Choose inference stack
12. Calibrate threshold
13. Choose final N
14. Measure context/token cost
15. Integrate production
16. Run regression evaluation