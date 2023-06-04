from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://cloud:cloud@db:5432/cloudb")
    SECRET_KEY: str = os.getenv("SECRET_KEY", os.urandom(32).hex())
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    POINT_MINUTES: int = os.getenv("POINT_MINUTES", 5)
    LOG_FILE: str = os.getenv("LOG_FILE","app/log/api.log")

settings = Settings()
print('Config:', settings.dict())
