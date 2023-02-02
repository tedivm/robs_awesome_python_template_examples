from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "library"
    debug: bool = False
