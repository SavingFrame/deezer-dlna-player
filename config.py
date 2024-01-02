from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEEZER_ARL: str
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
