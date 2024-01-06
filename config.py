import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEEZER_ARL: str
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    KAFKA_URL: str = "kafka://localhost:9092"
    MEDIA_URL: str
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MEDIA_PATH: str = "media"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
