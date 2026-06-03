from pathlib import Path

# Support multiple pydantic versions: older releases expose `BaseSettings`
# directly on `pydantic`, newer releases moved it to `pydantic-settings`.
try:
    from pydantic import BaseSettings, AnyUrl, PostgresDsn, validator
except Exception:
    from pydantic import AnyUrl, PostgresDsn, validator
    from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Multi-Agent AI Research Assistant"

    # Provide a sensible default for local development to avoid requiring
    # a running Postgres instance when starting the app for tests or dev.
    DATABASE_URL: str = f"sqlite:///{BASE_DIR.parent / 'dev.db'}"
    CHROMA_DB_DIR: str = str(BASE_DIR / "storage" / "chromadb")

    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    SECRET_KEY: str = "supersecretkey"

    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = BASE_DIR.parent / ".env"
        case_sensitive = True

settings = Settings()
