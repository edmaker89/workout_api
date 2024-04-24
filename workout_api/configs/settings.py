from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str= Field(default="postgresql+asyncpg://workout:workout@localhost:5460/workout")
    
settings = Settings()