"""
Проверка вводимог пользователем пароля после использования команды /user, для дальнейшего масштабирования вынесено в отдельный модуль
"""
from configs.config import admin_password


async def validate_admin_password(password: str) -> bool:
    return True if password == admin_password else False
