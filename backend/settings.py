from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Reads settings from .env file"""

    DB_FILE: str = "skbooks.db"
    GOOGLE_API_KEY: str | None = None
    LOG_LEVEL: str = "INFO"
    LOG_LEVELS: dict[str, str] = Field(default_factory=dict)

    @property
    def DB_URL(self) -> str:
        """returns the db url"""
        db_path = Path(__file__).parent.parent / self.DB_FILE
        return f"sqlite+aiosqlite:///{db_path.resolve()}"

    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
