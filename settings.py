from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_title: str = "FastAPI App"
    app_description: str = "A FastAPI application skeleton"
    app_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False 