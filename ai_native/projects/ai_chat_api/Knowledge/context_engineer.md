RAG:
    Retrieve information
Context Engineering:
    Decide
    what information
    how much information
    in what order
    in what representation
    to give the LLM


                    RAG
                     │
        ┌────────────┴────────────┐
        │                         │
    Retrieval                Context
        │                    Engineering
        │                         │
    Vector Search                MMR
       HNSW                     Dedup
       Recall                 Compression
        K                      Ordering
        │                     Token Budget
    Reranker                       │
        N                          │
        │                          │
        └────────────┬─────────────┘
                     ↓
                    LLM

A. Document-level compression: Nén tài liệu (Loại đơn giản nhất.)

D1 → relevant
D2 → relevant
D3 → irrelevant
D4 → relevant
D5 → irrelevant
=> Compression/filter:
                        D1
                        D2
                        D4
B. Sentence-level compression: Nén ở cấp độ câu
D1
 ├─ S1 irrelevant
 ├─ S2 relevant
 ├─ S3 irrelevant
 ├─ S4 relevant
 └─ S5 irrelevant
Ta chỉ lấy câu: S2 S4

C. LLM-based compression: Nén dựa trên LLM

-----------------------------------------------------------
| Thành phần          | Loại kiến thức                    |
| ------------------- | --------------------------------- |
| Embedding           | AI / Representation               |
| Vector Search       | Retrieval                         |
| HNSW                | Vector Database / Retrieval       |
| Recall@K            | Information Retrieval             |
| Reranker            | Retrieval                         |
| Diversity           | Retrieval Optimization            |
| Compression         | Context Optimization              |
| **Context Builder** | **RAG / LLM Context Engineering** |
| Prompt              | LLM Engineering                   |
| Generation          | LLM                               |

============================================================

                    QUERY
                      │
                      ▼
              ┌───────────────┐
              │   Retriever   │
              └───────┬───────┘
                      │
                      │ K
                      ▼
              ┌───────────────┐
              │   Reranker    │
              └───────┬───────┘
                      │
                      │ N
                      ▼
              ┌───────────────┐
              │   Diversity   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Compression   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │Context Builder│
              └───────┬───────┘
                      │
                      ▼
                    LLM

Retriever
→ maximize Recall

Reranker
→ maximize relevance ranking

Diversity
→ reduce redundancy

Compression
→ reduce unnecessary information

Context Builder
→ maximize usable information within token budget

LLM
→ generate answer


ContextBuilder không nên trở thành “god object”.
        -> Nó orchestration các bước context preparation