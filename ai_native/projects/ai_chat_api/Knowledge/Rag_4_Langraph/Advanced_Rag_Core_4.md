PHASE 4 — LangGraph

Chúng ta đã hiểu Agent bằng code thuần rồi mới học:
    State
    Node
    Edge
    Conditional Edge
    Persistence
    Checkpoint

PRODUCTION AGENT
│
├── 1. Agent Runtime
│   ├── Agent State
│   ├── Orchestration
│   ├── Loop Control
│   └── Termination
│
├── 2. Tool System
│   ├── Tool Definition
│   ├── Registry
│   ├── Tool Routing
│   ├── Validation
│   ├── Policy
│   └── Execution
│
├── 3. Reliability
│   ├── Retry
│   ├── Timeout
│   ├── Idempotency
│   ├── Rate Limit
│   └── Cancellation
│
├── 4. Context / Memory
│   ├── Context Builder
│   ├── Memory
│   └── RAG
│
├── 5. Safety
│   ├── Authorization
│   ├── Side-effect control
│   ├── Confirmation
│   └── Guardrails
│
├── 6. Observability
│   ├── Logs
│   ├── Traces
│   ├── Metrics
│   └── Cost / latency
│
├── 7. Evaluation
│   ├── Tool selection
│   ├── Tool arguments
│   ├── Task success
│   └── Final answer
│
└── 8. LangGraph
    └── implement explicit workflow/state transitions