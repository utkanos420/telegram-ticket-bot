"""
Загрузчик бота, инициализирующий основные необходимые компоненты

Важно: по умолчанию как менеджер состояний пользователь выбран MemoryStorage Dispatcher'а,
По необходимости можно закомментить его и раскомментить Redis, предварительно запустив докер, настроив .env докера в соотвествии передаваемых в него данных
"""
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from configs.config import settings

from redis.asyncio import Redis

bot = Bot(token=settings.bot_api_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# redis = Redis(host="localhost", port=6380, username="example_user", password="example")
# storage = RedisStorage(redis=redis)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)
