import logging
from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from functools import lru_cache

log = logging.getLogger("uvicorn")

class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    database_url: AnyUrl = None


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()