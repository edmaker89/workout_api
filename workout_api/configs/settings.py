from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str= Field(default="postgresql+asyncpg://postgres:reset666@localhost:5432/workout")
    
settings = Settings()