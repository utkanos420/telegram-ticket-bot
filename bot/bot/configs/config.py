"""
Основной конфигуратор окружения, который получает и валидирует параметры из .env

Главные параметры, необходимые для запуска, передаются в EnvSettings, а дополнительные параметры конфигурируются ниже как обычные экспортные переменные
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


# Класс, автоматически получающий значения из .venv и проверящий их тип
class EnvSettings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_api_key: str = ""


# Заполняется вручную
admin_ids: list[int] = []
admin_password: str = ""

# Объект конфига
settings = EnvSettings()
