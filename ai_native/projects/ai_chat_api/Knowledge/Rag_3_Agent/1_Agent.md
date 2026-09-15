1. Agent
LLM + ability to choose actions


2. Tool Calling
LLM → structured action request


3. Agent Loop (Core)
LLM
 ↓
Tool Call?
 ├── No → Answer
 └── Yes
      ↓
    Tool
      ↓
 Tool Result
      ↓
    LLM


Process:
                ┌──────────────────────┐
                │       Agent State    │
                └──────────┬───────────┘
                           ↓
                          LLM
                           ↓
                        Decision
                       /        \
                      /          \
                Final Answer    Tool Call
                    ↓              ↓
                    END           Tool
                                   ↓
                              Tool Result
                                   ↓
                              State Update
                                   ↓
                                  LLM

 --------------------------
|The problem we are facing:|
 --------------------------
1. User
   ↓
2. Load conversation state / context
   ↓
3. Context Planner
   ↓
4. Retrieval + Context Allocation + Context Builder
   ↓
5. LLM
   ↓
6. LLM quyết định:
      ├── Final answer
      └── Tool call
              ↓
7. Backend validate tool call
              ↓
8. Execute tool
              ↓
9. Tool result
              ↓
10. Update agent state
              ↓
11. LLM
      ├── Tool call → loop again
      └── Final answer → END