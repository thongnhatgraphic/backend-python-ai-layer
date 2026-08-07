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

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
