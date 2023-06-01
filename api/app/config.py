from pydantic import BaseSettings
import os
def cal_payment(dif_location: int):
    return 100*dif_location
class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", os.urandom(32).hex())
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    POINT_MINUTES: int = os.getenv("POINT_MINUTES", 5)

settings = Settings()
print('Config:', settings.dict())
