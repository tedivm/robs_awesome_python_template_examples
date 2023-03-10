from pydantic import BaseSettings

from .db import DatabaseSettings


class Settings(BaseSettings, DatabaseSettings):
    project_name: str = "full"
    debug: bool = False
