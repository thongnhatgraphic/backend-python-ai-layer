AgentRunner

    User
    ↓
    LLM
    ↓
    Tool call
    ↓
    Tool result
    ↓
    LLM
    ↓
    Tool call
    ↓
    Tool result
    ↓
    Final answer


Ví dụ: Agent chạy 5 bước.
    Step 1: gọi weather
    Step 2: lấy user name
    Step 3: tính toán
    Step 4: gọi một tool khác
    Step 5: trả lời

Trong lúc đó, Agent phải giữ được:
- user đang hỏi gì?
- messages hiện tại là gì?
- tool nào đã gọi?
- kết quả tool là gì?
- đang ở step bao nhiêu?
- đã có final answer chưa?
- có bị lỗi không?



0.0s
Agent bắt đầu

state:
step = 0
    status = RUNNING
    messages = [system, user]
    0.5s
    LLM quyết định gọi get_weather

state:
step = 1
    status = RUNNING
    messages += assistant(tool_call)
    0.7s
    Weather tool trả kết quả

state:
step = 1
    status = RUNNING
    messages += tool(result)
    1.0s
    LLM lại được gọi
    1.5s
    LLM quyết định gọi calculate_sum

state:
step = 2
    status = RUNNING
    messages += assistant(tool_call)
    1.7s
    Tool trả kết quả
    2.0s
    LLM trả final answer

state:
step = 2
    status = COMPLETED






             STATE
               │
               ▼
             LLM
               │
          decision
               │
       ┌───────┴───────┐
       │               │
    final            tool_call
       │               │
       ▼               ▼
   COMPLETED        ToolExecutor
                       │
                       ▼
                   tool result
                       │
                       ▼
                  STATE UPDATE
                       │
                       └──────→ LLM