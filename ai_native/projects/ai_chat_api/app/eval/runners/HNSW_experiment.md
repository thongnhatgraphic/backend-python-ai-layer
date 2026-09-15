HNSW Experiment #1

Corpus:
5,183 documents

Queries:
300

K:
20

Embedding:
nomic-embed-text (768)

Index:
HNSW
m=16
ef_construction=64

Results:
ef=10  → 81.55%
ef=20  → 87.70%
ef=40  → 89.03%
ef=80  → 89.70%
ef=100 → 89.70%

Exact baseline:
89.70%