from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_api_key: str = "xxx"


admin_ids: list[int] = [1710396755]

settings = Settings()
