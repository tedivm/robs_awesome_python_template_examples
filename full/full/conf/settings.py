from .db import DatabaseSettings


class Settings(DatabaseSettings):
    project_name: str = "full"
    debug: bool = False
