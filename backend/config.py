import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEEZER_ARL: str
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5674/"
    MEDIA_URL: str
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MEDIA_PATH: str = "media"
    REDIS_URL: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    version: int = 1
    disable_existing_loggers: bool = False
    level: str = "DEBUG"
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(name)s] %(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "level": "DEBUG",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "aio_pika": {"handlers": ["default"], "level": "INFO"},
        "aiormq": {"handlers": ["default"], "level": "INFO"},
        "async_upnp_client": {"handlers": ["default"], "level": "INFO"},
        "websockets": {"handlers": ["default"], "level": "INFO"},
        "upnp_listener": {"handlers": ["default"], "level": "INFO"},
        "upnp.discovery": {"handlers": ["default"], "level": "INFO"},
        "task_worker": {"handlers": ["default"], "level": "INFO"},
    }


log_config = LogConfig()
