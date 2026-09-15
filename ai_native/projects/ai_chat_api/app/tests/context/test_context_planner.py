from ollama import Client

from app.context.context_planner import ContextPlanner
from app.tests.context.context_planner_cases import CONTEXT_PLANNER_CASES
from app.core.settings import settings
from app.services.ollama_service import OllamaService

# def build_planner() -> ContextPlanner:
#     client = Client(host=settings.OLLAMA_HOST)

#     llm = OllamaService(
#         client=client,
#     )

#     return ContextPlanner(llm=llm)


# def evaluate_case(
#     planner: ContextPlanner,
#     case: dict,
# ) -> bool:

#     result = planner.plan(case["query"])

#     expected = case["expected"]

#     actual = {
#         "memory": result.memory.importance,
#         "rag": result.rag.importance,
#         "history": result.history.importance,
#     }

#     passed = actual == expected

#     print(f"\nCASE: {case['name']}")
#     print(f"QUERY: {case['query']}")
#     print(f"EXPECTED: {expected}")
#     print(f"ACTUAL:   {actual}")
#     print(f"RESULT:   {'PASS' if passed else 'FAIL'}")

#     return passed


def main():
    ollama_client = Client(host=settings.OLLAMA_HOST)

    llm = OllamaService(
        client=ollama_client,
    )

    planner = ContextPlanner(
        llm=llm,
    )

    test_cases = [
        "What is HNSW and why did we choose it?"
        # "One hour age, World news reports indicate that an earthquake has occurred in Japan."
        # "Do you remember who I am?",
        # "What project am I currently working on?",
        # "What is the mechanism of action of aspirin?",
        # "Explain what HNSW is.",
        # "Continue the architecture we discussed earlier.",
        # "What did we decide about the reranker?",
        # "Hello, how are you?",
        # "What is 2 + 2?",
        # "Tell me about our company's product documentation.",
        # "I prefer Python over JavaScript. Please remember that.",
    ]

    for index, query in enumerate(test_cases, start=1):
        print(f"\n===== CASE {index} =====")
        print("QUERY:", query)

        result = planner.plan(query)

        print(result.model_dump())


# def main():
#     planner = build_planner()

#     passed_count = 0

#     for case in CONTEXT_PLANNER_CASES:
#         if evaluate_case(planner, case):
#             passed_count += 1

#     total = len(CONTEXT_PLANNER_CASES)

#     print("\n===== CONTEXT PLANNER EVALUATION =====")
#     print(f"passed: {passed_count}/{total}")
#     print(f"accuracy: {passed_count / total:.2%}")


if __name__ == "__main__":
    main()
