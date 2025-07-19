from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Reads settings from .env file"""

    # When running with `uv run` from the `backend` directory, the CWD is `backend`,
    # so we go up one level to find the .env file in the project root.
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore"
    )
    db_file: str = "skbooks.db"

    @property
    def db_url(self) -> str:
        """returns the db url"""
        # We assume the db file is in the project root, which is the parent of the `backend` dir.
        db_path = Path(__file__).parent.parent / self.db_file
        return f"sqlite+aiosqlite:///{db_path.resolve()}"


@lru_cache
def get_settings() -> Settings:
    """returns the settings"""
    return Settings()


settings = get_settings()
