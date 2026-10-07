Tool Execution Error
│
├── Validation Error
│      └── ❌ no retry
│
├── Programming / Permanent Error
│      └── ❌ no retry
│
└── Transient Error
       ├── timeout
       ├── connection error
       ├── 429
       └── 5xx
              ↓
           ✅ retry

1. Trước tiên: hiểu “lỗi được show ở đâu”
    Tool
    ↓
    Executor
    ↓
    Agent / API
    ↓
    User

Và lỗi có thể được xử lý khác nhau ở từng tầng.

Ví dụ:
Pydantic ValidationError

Backend developer cần biết chi tiết:
a='Hello'
expected=int

User có thể chỉ cần: "The tool could not process the requested input."

"Còn LLM có thể nhận một tool error có cấu trúc để tự điều chỉnh request."

Developer-facing error ≠ User-facing error ≠ Agent-facing error
(Lỗi dành cho nhà phát triển ≠ Lỗi dành cho người dùng ≠ Lỗi dành cho nhân viên hỗ trợ)


                    ToolExecutor
                         │
              ┌──────────┴──────────┐
              │                     │
          Validation            Execution
              │                     │
              ↓                     ↓
       ValidationError         Runtime error
              │                     │
              ↓                     ↓
     ToolValidationError     classify error
              │                     │
              ↓                 ┌───┴────┐
         no retry               │        │
                                ↓        ↓
                           transient   permanent
                                │        │
                                ↓        ↓
                              retry    no retry

ValidationError
    → sai input

TransientError
    → có khả năng tự hết

TimeoutError
    → có khả năng thử lại

PermanentError
    → thử lại cũng không giúp



