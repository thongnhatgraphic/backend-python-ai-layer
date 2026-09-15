User message
   │
   ├── Memory retrieval/rerank
   │
   └── RAG retrieval/rerank/gate
            │
            ▼
      Candidate context
            │
            ▼
     Dynamic Allocation
            │
            ▼
       ContextBuilder
            │
            ▼
            LLM

            

Context Engineering:

    Context Engineering = thiết kế và kiểm soát toàn bộ thông tin mà LLM được phép nhìn thấy trước khi reasoning.

    Context Engineering is a process. Include design and control all information, That really helpfull for LLM to see before reasoning

ContextBuilder không nên mù quáng:

Nó phải kiểm tra:
    Document 1 → phù hợp
    Document 2 → phù hợp
    Document 3 → phù hợp
    Document 4 → quá dài
    Document 5 → duplicate


Ví dụ request hiện tại có:
    Conversation history
    Long-term memory
    Retrieved documents
    User query
    System instructions


Khi có RAG, ta phải phân biệt:
    Memory budget
    RAG budget
    History budget
    Instruction budget

Ví dụ giả sử context budget:
    History       1,000
    Memory          500
    RAG           2,000
    System          300
    User            100
    ----------------
    Total          3,900


Đây là điểm cực kỳ quan trọng:
    Retriever quyết định candidate
    Reranker quyết định ranking
    ContextBuilder quyết định context budget

----------Phân Biệt--------------

User
 ↓
ChatService
 ├── ConversationMemory
 ├── Long-term Memory
 ├── ContextBuilder
 └── LLM

Nó chủ yếu giúp:
LLM hiểu conversation + hiểu user.



Sau khi thêm RAG:
                       ┌── Memory
                       │
User → Retrieval ──────┼── RAG Documents
                       │
                       └── History
                              ↓
                        ContextBuilder
                              ↓
                             LLM


Bây giờ LLM có:

Who is the user?
        +
What has been discussed?
        +
What external evidence is relevant?
        ↓
     Reasoning

     
     