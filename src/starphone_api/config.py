from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_ECHO: bool
    DATABASE_CONNECT_ARGS: dict
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
