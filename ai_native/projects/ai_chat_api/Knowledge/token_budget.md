Giả sử model có:
    Context window = 32K tokens

Nhưng request của chúng ta đã dùng:
    System prompt       = 2K
    Conversation history = 4K
    User query           = 500
    Retrieved documents  = 20K

Tổng: 26.5K

Còn: 32K - 26.5K = 5.5K Cho generation

    retrieval
        ↓
    context too large
        ↓
    LLM request
        ↓
    truncate / error / expensive request 

    "Context Budgeting."

