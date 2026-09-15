- Dense Retrieval Baseline v1 (Exact search):
Embedding: nomic-embed-text
Dimension: 768
Corpus: 5,183 docs
Evaluation: 300 queries

    === Retrieval Evaluation ===
    Recall@5: 0.7601 (76.01%)
    Recall@10: 0.8455 (84.55%)
    Recall@20: 0.8970 (89.70%)
    Recall@50: 0.9233 (92.33%)
    Recall@100: 0.9417 (94.17%)


--------------------------------------------------
            <!-- HNSW search -->

Embedding: nomic-embed-text
Dimension: 768
Corpus: 5,183 docs
Evaluation: 300 queries

# === Retrieval Evaluation ===
# Recall@20: 0.8155 (81.55%) ef_search = 10
# Recall@20: 0.8770 (87.70%) ef_search = 20
# Recall@20: 0.8903 (89.03%) ef_search = 40
# Recall@20: 0.8970 (89.70%) ef_search = 80
# Recall@20: 0.8970 (89.70%) ef_search = 100


Với K = 20 Thì Recall của ef_search= 40 và 80 tương đối 
10 → recall thấp
20 → còn thấp
40 → gần exact
80 → exact
100 → không cải thiện so với 80

Ta tập trung vào 40 và 80

| Configuration | Recall@20 |      P50 |      P95 |
| ------------- | --------: | -------: | -------: |
| Exact         |    89.70% | baseline | baseline |
| HNSW ef=40    |    89.03% |        ? |        ? |
| HNSW ef=80    |    89.70% |        ? |        ? |

<mark>
    # ef_search=40 mất 0.67pp Recall nhưng có latency thấp hơn X ms.
</mark>

<mark>
    # ef_search=80 đạt exact-search Recall nhưng phải trả thêm Y ms.
<mark/>

Chúng ta đã chạy HNSW cho 300 queries và
# 300 queries
# K=20, EF = 40 ,P50: 47.06139449994225ms
# K=20, EF = 40 ,P95: 51.239878650045284ms
# K=20, EF = 80 ,P50: 67.07643300016571ms
# K=20, EF = 80 ,P95: 71.37749501665166ms

Recall@20 = 89.03%
P50        = 47.06 ms
P95        = 51.24 ms

Recall@20 = 89.70%
P50        = 67.08 ms
P95        = 71.38 ms

40 → 80

Cho: Recall
89.03 → 89.70
+0.67 percentage point

nhưng latency:

P50:
47.06 → 67.08
≈ +20.02 ms

P95:
51.24 → 71.38
≈ +20.14 ms

1. Nếu business requirement là P95 < 60ms
    Thì:
    ef=40  → 51.24ms ✅
    ef=80  → 71.38ms ❌
    → 40 thắng rõ ràng.

2. Nếu business requirement là P95 < 80ms
    Cả hai đều hợp lệ:
    40 → 51.24ms ✅
    80 → 71.38ms ✅

    Lúc đó chúng ta phải hỏi:
    Có đáng trả thêm ~20ms để lấy thêm 0.67 điểm Recall không?
    Đây chính là quyết định engineering.

HNSW Experiment:
        Exact
        Recall@20 = 89.70%

    HNSW
        ef=10 → 81.55%
        ef=20 → 87.70%
        ef=40 → 89.03%
        ef=80 → 89.70%
        ef=100 → 89.70%
    Latency
        ef=40:
        P50 = 47.06ms
        P95 = 51.24ms

        ef=80:
        P50 = 67.08ms
        P95 = 71.38ms

Latency:
        ef=40:
        P50 = 47.06ms
        P95 = 51.24ms

        ef=80:
        P50 = 67.08ms
        P95 = 71.38ms



# Exact Recall@20        = 89.70%

HNSW:
ef=10                  = 81.55%
ef=20                  = 87.70%
ef=40                  = 89.03%
ef=80                  = 89.70%
ef=100                 = 89.70%

Latency full workload:
ef=40 → P50 47.06ms / P95 51.24ms
ef=80 → P50 67.08ms / P95 71.38ms

-----------------------------Sumary-----------------------

Dataset       = SciFact
Queries       = 300
Retriever     = Dense HNSW
ef_search     = 40
Retrieval K   = 20
Final K       = 5
Metric        = Recall@5
