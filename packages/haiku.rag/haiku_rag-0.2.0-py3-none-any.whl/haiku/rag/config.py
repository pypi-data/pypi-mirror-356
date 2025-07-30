import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

from haiku.rag.utils import get_default_data_dir

load_dotenv()


class AppConfig(BaseModel):
    ENV: str = "development"

    DEFAULT_DATA_DIR: Path = get_default_data_dir()
    MONITOR_DIRECTORIES: list[Path] = []

    EMBEDDINGS_PROVIDER: str = "ollama"
    EMBEDDINGS_MODEL: str = "mxbai-embed-large"
    EMBEDDINGS_VECTOR_DIM: int = 1024

    CHUNK_SIZE: int = 256
    CHUNK_OVERLAP: int = 32

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    @field_validator("MONITOR_DIRECTORIES", mode="before")
    @classmethod
    def parse_monitor_directories(cls, v):
        if isinstance(v, str):
            if not v.strip():
                return []
            return [
                Path(path.strip()).absolute() for path in v.split(",") if path.strip()
            ]
        return v


# Expose Config object for app to import
Config = AppConfig.model_validate(os.environ)
