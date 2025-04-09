from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    TOKEN_SECRET: str
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int = 3306

    class Config:
        env_file = ".env"

settings = Settings()