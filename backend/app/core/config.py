from pathlib import Path
from pydantic import BaseSettings, AnyUrl, PostgresDsn, validator

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Multi-Agent AI Research Assistant"

    DATABASE_URL: str
    CHROMA_DB_DIR: str = str(BASE_DIR / "storage" / "chromadb")

    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    SECRET_KEY: str = "supersecretkey"

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = BASE_DIR.parent / ".env"
        case_sensitive = True

settings = Settings()
