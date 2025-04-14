from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from configs.config import settings

bot = Bot(token=settings.bot_api_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = MemoryStorage()

dp = Dispatcher(storage=storage)
