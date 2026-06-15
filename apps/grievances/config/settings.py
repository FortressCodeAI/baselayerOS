from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BaseLayerOS Grievance Assistant"
    debug: bool = True

    database_url: str = "sqlite:///./data/baselayeros.db"
    log_dir: Path = Path("data/logs")
    attachment_dir: Path = Path("data/attachments")
    policy_dir: Path = Path("config/policies")
    deadlines_file: Path = Path("config/deadlines.yaml")

    class Config:
        env_prefix = "BLOS_"
        env_file = ".env"


settings = Settings()
settings.log_dir.mkdir(parents=True, exist_ok=True)
settings.attachment_dir.mkdir(parents=True, exist_ok=True)
settings.policy_dir.mkdir(parents=True, exist_ok=True)
settings.deadlines_file.parent.mkdir(parents=True, exist_ok=True)
