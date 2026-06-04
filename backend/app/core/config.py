import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine the absolute path to the backend directory where .env resides
_current_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.dirname(os.path.dirname(_current_dir))
_env_path = os.path.join(_backend_dir, ".env")

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/datasense_db")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    model_config = SettingsConfigDict(env_file=_env_path, extra="ignore")

settings = Settings()

