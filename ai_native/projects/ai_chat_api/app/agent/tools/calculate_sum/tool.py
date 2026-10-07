def calculate_sum(a: int, b: int) -> dict:
    return {"result": a + b}


# User
#  │
#  │ "Hãy tính tổng 10 và 20"
#  ↓
# AgentRunner
#  │
#  │ messages + tools
#  ↓
# LLM
#  │
#  │ ToolCall:
#  │ calculate_sum
#  │ {"a":10,"b":20}
#  ↓
# AgentRunner
#  │
#  ├── Registry.resolve("calculate_sum")
#  │
#  ├── Validate arguments
#  │
#  └── Execute calculate_sum(a=10,b=20)
#                          │
#                          ↓
#                     {"result":30}
#                          │
#                          ↓
#              append role="tool"
#                          │
#                          ↓
#                       messages
#                          │
#                          ↓
#                         LLM
