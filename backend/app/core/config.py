from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    cors_origins: list[str] = ["http://localhost:5173"]

    resume_data_dir: Path = BACKEND_DIR / "data" / "resume"
    index_dir: Path = BACKEND_DIR / "data" / "index"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"


settings = Settings()
