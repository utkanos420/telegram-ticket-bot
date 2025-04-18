"""
Основной модуль состояний администратора, обрабатывающий вводы администратора
"""
from loguru import logger
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.telegram_db_methods.db_methods import DBMethods
from keyboards.dynamic_keyboards import mute_user_by_id

from bot_utils.sendreport import notice_muted_user

from templates.template_engine import render_template

from states.admin_states import AdminStates

db_methods = DBMethods()


logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<level>[{time:YYYY-MM-DD HH:mm:ss}] #{level:<8} {file.name}:"
           "{line} - {name} - {message}</level>",
    level="DEBUG",
    colorize=True
)

admin_router = Router()


@admin_router.callback_query(lambda c: c.data.startswith("show_report_by_id_"), StateFilter(AdminStates.global_state))
async def return_the_report_by_id(callback: CallbackQuery, state: FSMContext):
    post_id_str = callback.data.removeprefix("show_report_by_id_")
    post_id = int(post_id_str)

    db = DBMethods()
    report = await db.get_user_report_by_id(post_id)

    if report:
        await callback.message.answer(
            f"Репорт №{report.id}:\n"
            f"Причина: {report.report_reason}\n"
            f"Описание: {report.report_description or 'Нет описания'}\n"
            f"Этаж: {report.report_floor or ''}\n"
            f"Аудитория: {report.report_audience or ''}\n",
            reply_markup=mute_user_by_id(report.user_id)
        )
    else:
        await callback.message.answer("Репорт не найден.")


@admin_router.callback_query(lambda c: c.data.startswith("mute_user_by_id_"), StateFilter(AdminStates.global_state))
async def mute_user(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.removeprefix("mute_user_by_id_")
    db = DBMethods()
    await db.mute_user_by_id(user_id=user_id)
    await callback.message.answer(f"Пользователь с id {user_id} заблокирован")
    await notice_muted_user(user_id)


@admin_router.message(Command("unmute"), StateFilter(AdminStates.global_state))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id):
        return

    await message.answer(render_template("admin_answers/unmute.html"), parse_mode="HTML")
    await state.set_state(AdminStates.get_user_id)


@admin_router.message(F.text, StateFilter(AdminStates.get_user_id))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id):
        return

    await db_methods.unmute_user_by_id(user_id=message.text)
    await message.answer("Пользователь разблокирован")
    await state.set_state(AdminStates.global_state)
