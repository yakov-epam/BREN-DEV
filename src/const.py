from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path
from enum import StrEnum
from modules import DB


class AppEnv(StrEnum):
    """
    Application environment type enum.
    """

    DEV = "dev"
    PROD = "prod"


load_dotenv(dotenv_path=Path(__file__).parent.parent / "env" / ".env")


class AppSettings(BaseModel):
    host: str = Field(default="0.0.0.0", title="Application host")
    port: int = Field(default=8080, title="Application port")
    title: str = Field(default="Books API", title="Application title")
    disable_swagger: bool = Field(default=False, title="Whether to disable swagger docs")
    disable_redoc: bool = Field(default=True, title="Whether to disable ReDoc docs")
    latest_v1: str = Field(default="1.0.0", title="Latest version of V1 API")


class DBSettings(BaseModel):
    host: str = Field(default="postgres")
    port: int = Field(default=5432)
    name: str = Field(default="app")
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")
    env: AppEnv = Field(default=AppEnv.DEV)

    app: AppSettings = Field(default_factory=AppSettings, title="Application settings")
    db: DBSettings = Field(title="Database settings")


SETTINGS = Settings()  # noqa
DATABASE = DB(
    host=SETTINGS.db.host,
    port=SETTINGS.db.port,
    database=SETTINGS.db.name,
    user=SETTINGS.db.username,
    password=SETTINGS.db.password,
)
