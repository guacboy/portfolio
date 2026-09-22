from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cors_origins: list[str] = ["http://localhost:5173"]

    resume_data_dir: Path = BACKEND_DIR / "data" / "resume"
    index_dir: Path = BACKEND_DIR / "data" / "index"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_path: Path = BACKEND_DIR / "models" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"
    llm_context_size: int = 4096
    llm_max_tokens: int = 512

    retrieval_top_k: int = 4
    # FAISS L2 distance; lower = more similar. Below this, treat the query as in-scope.
    retrieval_distance_threshold: float = 1.6


settings = Settings()
