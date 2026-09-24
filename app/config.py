from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Task Tracker API"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tasktracker"
    SECRET_KEY: str = "change-me-in-production-supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
