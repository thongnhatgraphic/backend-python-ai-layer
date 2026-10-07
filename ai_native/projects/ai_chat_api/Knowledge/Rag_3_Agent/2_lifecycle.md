architecture pipeline:
                         ┌──────────────┐
                         │     LLM      │
                         └──────┬───────┘
                                │
                           Tool Call
                                ↓
                    ┌────────────────────┐
                    │    AgentRunner     │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   ToolRegistry     │
                    └─────────┬──────────┘
                              │
                         Resolve tool
                              ↓
                    ┌────────────────────┐
                    │ Argument Validator │
                    └─────────┬──────────┘
                              │
                           valid?
                              ↓
                    ┌────────────────────┐
                    │ Authorization /    │
                    │ Policy             │
                    └─────────┬──────────┘
                              │
                           allowed?
                              ↓
                    ┌────────────────────┐
                    │   ToolExecutor     │
                    │                    │
                    │ timeout            │
                    │ retry              │
                    │ logging            │
                    │ metrics            │
                    └─────────┬──────────┘
                              │
                              ↓
                         Tool function
                              │
                              ↓
                         ToolResult
                              │
                              ↓
                            LLM



LLM Output
     ↓
Untrusted Input
     ↓
Tool Registry
     ↓
Schema Validation
     ↓
Authorization / Policy
     ↓
Timeout
     ↓
Retry policy
     ↓
Execute
     ↓
Tool Result
     ↓
Agent State
     ↓
LLM