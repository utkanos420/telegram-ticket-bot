"""
Модуль, отвечающий за обработку пользователя до передачи в стейты по роутерам

Мидлварь проверяет, есть ли в БД пользователь, и если нет, создает

Мидлварь проверяет, указан ли ID пользователя как ID администратора, и если да, заранее переводит его в состояния администратора
"""
from loguru import logger
from datetime import datetime
from typing import Callable, Any, Awaitable, Dict
from random import randint
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message
from aiogram.filters import StateFilter
from aiogram import BaseMiddleware

from database.telegram_db_methods.db_methods import DBMethods
from states.user_states import UserStates
from states.admin_states import AdminStates

from configs.config import admin_ids

from keyboards.keyboard_utils import create_report_keyboard

from templates import render_template


logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<level>[{time:YYYY-MM-DD HH:mm:ss}] #{level:<8} {file.name}:"
           "{line} - {name} - {message}</level>",
    level="DEBUG",
    colorize=True
)


class UserInternalIdMiddleware(BaseMiddleware):
    def __init__(self):
        self.db_methods = DBMethods()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        state: FSMContext = data.get("state")

        if user:
            user_id = user.id
            username = user.username

            existing_user = await self.db_methods.get_user(user_id)

            if not existing_user:
                created_user = await self.db_methods.create_user(user_id, username)
                logger.debug("User created")

            data["user_id"] = user_id
            data["user_username"] = username

            if user_id in admin_ids:
                await state.set_state(AdminStates.global_state)
            else:
                await state.set_state(UserStates.global_state)

            logger.debug("Middleware has processed the user.")
        else:
            logger.warning("No user information found in the event data.")

        return await handler(event, data)


start_router = Router()
start_router.message.middleware(UserInternalIdMiddleware())


@start_router.message(CommandStart(), StateFilter(None))
async def start(message: types.Message, state: FSMContext):

    if message.chat.type != "private":
        return

    if message.from_user.id in admin_ids:
        await message.answer(render_template("admin_answers/welcome.html"), parse_mode="HTML")
    else:
        await message.answer(render_template("user_answers/welcome.html"), parse_mode="HTML", reply_markup=create_report_keyboard())


@start_router.message(F.text, StateFilter(None))
async def start(message: types.Message, state: FSMContext):

    if message.chat.type != "private":
        return

    if message.from_user.id in admin_ids:
        await message.answer(render_template("admin_answers/welcome.html"), parse_mode="HTML")
    else:
        await message.answer(render_template("user_answers/welcome.html"), parse_mode="HTML", reply_markup=create_report_keyboard())
