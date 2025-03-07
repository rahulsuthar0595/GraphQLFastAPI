from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: str = False
    SQLALCHEMY_DATABASE_URI: str = None
    GRAPHQL_IDE: str = "graphiql"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
