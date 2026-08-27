from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_provider: str = "local"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    dense_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    top_k_dense: int = 8
    top_k_bm25: int = 8
    top_k_rerank: int = 5

    chunk_size: int = 700
    chunk_overlap: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
