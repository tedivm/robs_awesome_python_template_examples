from quasiqueue import Settings as QuasiQueueSettings

from .cache import CacheSettings
from .db import DatabaseSettings


class Settings(QuasiQueueSettings, DatabaseSettings, CacheSettings):
    project_name: str = "full"
    debug: bool = False
