from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DEFAULT_MODEL: str
    OLLAMA_HOST: str
    OLLAMA_MODEL: str
    DATABASE_URL: str
    MEMORY_SAVE_THRESHOLD: float
    MAX_CONTEXT_MESSAGES: int
    MAX_RETRIEVAL_MEMORIES: int
    MAX_SUMMARIZE_MESSAGES: int
    OLLAMA_EMBEDDING_MODEL: str
    VECTOR_SEARCH_K: int
    RERANKER_LIMIT: int
    RERANKER_THRESHOLD: float
    OLLAMA_NUM_CTX: int
    OLLAMA_NUM_PREDICT: int
    CONTEXT_SAFETY_MARGIN: int
    TOKENIZER_MODEL: str
    RAG_HNSW_EF_SEARCH: int
    RAG_RELEVANCE_THRESHOLD: float
    CONTEXT_PLANNER_HISTORY_TOKENS: int
    CONTEXT_MEMORY_MAX_USEFUL_TOKENS: int
    CONTEXT_RAG_MAX_USEFUL_TOKENS: int
    CONTEXT_HISTORY_MAX_USEFUL_TOKENS: int

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
