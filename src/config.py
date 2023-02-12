import os
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, RedisDsn, validator


class Settings(BaseSettings):
    ENVIRONMENT: str
    DEBUG: bool = False
    SERVICE_NAME: str
    ADMIN_PATH: str = "/admin"
    BACKEND_CORS_ORIGINS: List[str] = ['*']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MODULES: List[str] = ["core", "parking"]

    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None
    SECRET_KEY: Optional[str] = None
    API_KEY: str
    API_KEY_HEADER_NAME: Optional[str] = 'token'
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_POOL_MIN_SIZE: int = 1
    POSTGRES_POOL_MAX_SIZE: int = 5

    REDIS_SERVER: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    REDIS_USER: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: Optional[str] = None

    TELEMETRY_ENABLE: bool = False
    TELEMETRY_DEBUG: bool = False
    TELEMETRY_AGENT_HOST: Optional[str] = None
    TELEMETRY_AGENT_PORT: Optional[str] = None

    METRICS_ENABLE: bool = False

    SENTRY_DSN: Optional[str] = None

    REDIS_URL: Optional[RedisDsn] = None
    TORTOISE_CONFIG: Optional[dict] = None

    STATIC_URL: str = os.path.join("/", "static/")
    STATIC_ROOT: str = os.path.join(BASE_DIR, "static")

    SCREENSHOT_URL: str = os.path.join("/", "screenshot/")
    SCREENSHOT_ROOT: str = os.path.join(BASE_DIR, "screenshot")
    # Ограничение в 3 камеры задано т.к. всего было три камеры и больше не планировалось.
    LIMIT_CAMERAS: Optional[int] = 3
    # period run task creating screenshot in seconds
    PERIODIC_GET_SCREENSHOT_MINUTE: Optional[int] = 2
    PERIODIC_GET_FREE_PLACE_MINUTE: Optional[int] = 1
    CACHE_SCREEN_KEY: Optional[str] = 'screen'
    CACHE_KEY_FREE_PLACE: Optional[str] = 'counter'
    CACHE_TTL: Optional[int] = 180

    LOCK_SCREEN_TASK_KEY: Optional[str] = "screen_task"
    LOCK_FREE_PLACES_TASK_KEY: Optional[str] = "free_place_task"

    PARKING_CONTROLLER_ENABLED: bool = True
    PARKING_CONTROLLER_WS_URL: Optional[str] = "ws://10.0.2.10:6432"

    AWS_S3_ENDPOINT_URL: str
    AWS_S3_REGION_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str


    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("TELEMETRY_AGENT_HOST", pre=True)
    def assemble_telemtry_agent_host(cls, v: Optional[str], values: Dict[str, Any]):
        if not isinstance(v, str) and values.get("TELEMETRY_ENABLE") and not values.get("TELEMETRY_DEBUG"):
            raise ValueError(v)
        return v

    @validator("TELEMETRY_AGENT_PORT", pre=True)
    def assemble_telemtry_agent_port(cls, v: Optional[str], values: Dict[str, Any]):
        if not isinstance(v, str) and values.get("TELEMETRY_ENABLE") and not values.get("TELEMETRY_DEBUG"):
            raise ValueError(v)
        return v

    @validator("SECRET_KEY", pre=True)
    def assemble_secret_key(cls, v: Optional[str], values: Dict[str, Any]):
        if not isinstance(v, str) and values.get("ENVIRONMENT") != "local":
            raise ValueError(v)
        return v

    @validator("SENTRY_DSN", pre=True)
    def assemble_sentry_dsn(cls, v: Optional[str], values: Dict[str, Any]):
        if not isinstance(v, str) and values.get("ENVIRONMENT") != "local":
            raise ValueError(v)
        return v

    @validator("ACCESS_TOKEN_EXPIRE_MINUTES", pre=True)
    def assemble_access_token_expire_minutes(cls, v: Optional[str], values: Dict[str, Any]):
        if not isinstance(v, str) and values.get("ENVIRONMENT") != "local":
            raise ValueError(v)
        return v

    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]):
        if isinstance(v, str):
            return v
        elif (
                values.get("REDIS_USER") and
                values.get("REDIS_PASSWORD") and
                values.get("REDIS_SERVER") and
                values.get("REDIS_PORT") and
                values.get('REDIS_DB')
        ):
            return RedisDsn.build(
                scheme="redis",
                user=values.get("REDIS_USER"),
                password=values.get("REDIS_PASSWORD"),
                host=values.get("REDIS_SERVER"),
                port=values.get("REDIS_PORT"),
                path=f"/{values.get('REDIS_DB') or ''}",
            )
        else:
            raise ValueError(v)

    @validator("TORTOISE_CONFIG", pre=True)
    def assemble_tortoise_config(cls, v: Optional[Dict[str, Dict[str, Any]]], values: Dict[str, Any]):
        if isinstance(v, dict):
            return v
        modules_models = [f"{m}.models" for m in values.get("MODULES", [])]
        modules_models.append("aerich.models")
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": values.get("POSTGRES_DB_HOST"),
                        "port": values.get("POSTGRES_DB_PORT"),
                        "user": values.get("POSTGRES_DB_USER"),
                        "password": values.get("POSTGRES_DB_PASSWORD"),
                        "database": values.get("POSTGRES_DB_NAME"),
                        "minsize": values.get("POSTGRES_POOL_MIN_SIZE"),
                        "maxsize": values.get("POSTGRES_POOL_MAX_SIZE"),
                        "statement_cache_size": 0,
                    },
                },
            },
            "apps": {
                "models": {
                    "models": modules_models,
                    "default_connection": "default",
                }
            },
            "use_tz": False,
            "timezone": "UTC",
        }

    class Config:
        case_sensitive = True
        env_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".env",
        )


settings = Settings()
TORTOISE_CONFIG = settings.TORTOISE_CONFIG
