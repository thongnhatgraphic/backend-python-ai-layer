System Prompt:
    |
    |
    Nó còn quy định:
        Vai trò (Role)
        Hành vi (Behavior)
        Quy tắc (Rules)
        Giới hạn (Constraints)
        Mục tiêu (Goal)

System Prompt
+
Rules
+
Output Format
+
Tool Descriptions
+
Context
+
Current Question

Phải đủ độ phức tạp mới tách thành 1 module riêng

--------------------------------------------------------
Backend

ConversationMemory
        │
        ▼
ContextBuilder
        │
        ▼
messages ⭐⭐⭐
        │
        ▼
Prompt Formatting ⭐⭐⭐
        │
        ▼
Tokenizer ⭐⭐⭐
        │
        ▼
Token IDs
        │
        ▼
Embedding
        │
        ▼
Transformer
        │
        ▼
Next Token


Role không chỉ để. Biết ai nói.

Mà còn để. Biết ai có quyền hơn.
                            System
                                ▲

                            Developer
                                ▲

                            User
                                ▲

                            Assistant


### USER ###                
messages
        │
        ▼
Apply Chat Template
        │
        ▼
Prompt (có Special Tokens)
        │
        ▼
Tokenizer
        │
        ▼
Token IDs
        │
        ▼
Embeddings
        │
        ▼
Transformer
        │
        ▼
Next Token            