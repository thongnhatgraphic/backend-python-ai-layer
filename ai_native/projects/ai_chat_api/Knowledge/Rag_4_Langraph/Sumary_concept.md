| Thứ chúng ta đã có            | LangGraph concept         |
|-------------------------------|---------------------------|
| `AgentState`                  | Graph State               |
| `_run_loop()`                 | Graph execution           |
| `_handle_response()`          | Node/route logic          |
| `ResponseType`                | Routing condition         |
| ToolExecutor                  | Tool node / execution     |
| HITL                          | Interrupt / resume |
| Redis state                   | Checkpoint / persistence  |
| `step`                        | Iteration/state           |
| termination                   | END / routing             |
| AgentRunner                   | Graph orchestration       |



| Project của chúng ta          | LangGraph                 |
|---    ---                     |---                        |
| `AgentState`                  | State                     |
| `_handle_response()`          | Node/logic                |
| `_run_loop()`                 | Graph execution           |
| `if tool_calls`               | Conditional routing       |
| tool execution                | Tool node                 |
| `break`                       | END / termination         |

