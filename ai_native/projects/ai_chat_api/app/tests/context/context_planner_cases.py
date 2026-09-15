from app.context.context_priority import ContextImportance

CONTEXT_PLANNER_CASES = [
    {
        "name": "memory_identity",
        "query": "Do you remember who I am?",
        "expected": {
            "memory": ContextImportance.HIGH,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "memory_project",
        "query": "What project am I currently working on?",
        "expected": {
            "memory": ContextImportance.HIGH,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "rag_factual",
        "query": "What is the mechanism of action of aspirin?",
        "expected": {
            "memory": ContextImportance.NONE,
            "rag": ContextImportance.HIGH,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "rag_hnsw",
        "query": "Explain what HNSW is.",
        "expected": {
            "memory": ContextImportance.NONE,
            "rag": ContextImportance.HIGH,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "history_continue",
        "query": "Continue what we discussed earlier.",
        "expected": {
            "memory": ContextImportance.NONE,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.HIGH,
        },
    },
    {
        "name": "memory_and_history",
        "query": "What did we decide about the reranker?",
        "expected": {
            "memory": ContextImportance.HIGH,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.HIGH,
        },
    },
    {
        "name": "casual_chat",
        "query": "Hello, how are you?",
        "expected": {
            "memory": ContextImportance.NONE,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "simple_math",
        "query": "What is 2 + 2?",
        "expected": {
            "memory": ContextImportance.NONE,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "company_product",
        "query": "Tell me about our company's product documentation.",
        "expected": {
            "memory": ContextImportance.NONE,
            "rag": ContextImportance.HIGH,
            "history": ContextImportance.NONE,
        },
    },
    {
        "name": "store_preference",
        "query": "I prefer Python over JavaScript. Please remember that.",
        "expected": {
            "memory": ContextImportance.HIGH,
            "rag": ContextImportance.NONE,
            "history": ContextImportance.NONE,
        },
    },
]
