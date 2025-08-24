from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import BaseSettings


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="smtp_")

    host: str = Field(default="smtp.yandex.ru", title="SMTP host")
    port: int = Field(default=465, title="SMTP port")
    username: str = Field(default="", title="SMTP username")
    password: str = Field(default="", title="SMTP password")


smtp_settings = SMTPSettings()
