Router
      │
      ▼
ChatService
      │
      ├──────────────┐
      ▼              ▼
ConversationMemory   ContextBuilder
      │              │
      └──────┐       │
             ▼       ▼
         OllamaService
               │
               ▼
             LLM

            --------------------
                ChatService
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
ConversationMemory           ContextBuilder
      │                             │
      └──────────────┬──────────────┘
                     ▼
               OllamaService
                     ▼
                    LLM
                     ▼
                ChatService
                     ▼
ConversationMemory.save_assistant(...)

✅ ConversationMemory lưu lịch sử.
✅ ContextBuilder xây dựng context cho chatbot.
✅ MemoryExtractor đọc hội thoại và sinh ra Memory Candidate.
✅ MemoryStore lưu các Memory đã được trích xuất.