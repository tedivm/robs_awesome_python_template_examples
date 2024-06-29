from pydantic_settings import BaseSettings
from quasiqueue import Settings as QuasiQueueSettings

from .db import DatabaseSettings


class Settings(BaseSettings, QuasiQueueSettings, DatabaseSettings):
    project_name: str = "full"
    debug: bool = False
