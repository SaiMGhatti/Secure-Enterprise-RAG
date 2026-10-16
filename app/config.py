from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env", extra="ignore")

    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_timeout_seconds: float = 120.0

    candidate_k: int = 20
    top_k: int = 5
    # Cross-encoder score below which a chunk is treated as not relevant
    min_rerank_score: float = -2.0


settings = Settings()
