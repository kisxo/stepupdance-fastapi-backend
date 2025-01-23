from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    MONGO_HOST: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
