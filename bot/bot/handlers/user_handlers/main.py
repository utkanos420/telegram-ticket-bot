from loguru import logger
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from database.telegram_db_methods.db_methods import DBMethods
from templates import render_template

from states.user_states import UserStates, Anketa

from keyboards.keyboard_utils import floors_keyboard, audi_keyboard, reason_keyboard, skip_report_description

from bot_utils.sendreport import send_report_to_admins


logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<level>[{time:YYYY-MM-DD HH:mm:ss}] #{level:<8} {file.name}:"
           "{line} - {name} - {message}</level>",
    level="DEBUG",
    colorize=True
)

user_main_router = Router()
db_methods = DBMethods()


@user_main_router.message(Command("report"), StateFilter(UserStates.global_state))
async def create_report_from_command(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id):
        return

    await message.answer(render_template("user_answers/problem.html"), parse_mode="HTML")
    await message.answer("<b>Выберите ваш этаж:</b>", reply_markup=floors_keyboard(), parse_mode="HTML")


@user_main_router.callback_query(F.data == "create_report", StateFilter(UserStates.global_state))
async def create_report_from_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user_answers/problem.html"), parse_mode="HTML")
    await callback.message.answer("<b>Выберите ваш этаж:</b>", reply_markup=floors_keyboard(), parse_mode="HTML")


@user_main_router.callback_query(F.data == 'floor_3', StateFilter(UserStates.global_state))
async def handle_floor_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer("<b>Выберите вашу аудиторию:</b>", reply_markup=audi_keyboard(), parse_mode="HTML")
    await state.update_data(floor=3)
    await state.set_state(Anketa.get_auditory)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'aud_405', StateFilter(Anketa.get_auditory))
async def handle_audience_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer("<b>Выберите вашу проблему из списка:</b>", reply_markup=reason_keyboard(), parse_mode="HTML")
    await state.update_data(audi=405)
    await state.set_state(Anketa.get_trouble)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'sound', StateFilter(Anketa.get_trouble))
async def handle_reason_button(callback: CallbackQuery, state: FSMContext):

    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user_answers/problem_description.html"), parse_mode="HTML", reply_markup=skip_report_description())
    await state.update_data(trouble="sound")
    await state.set_state(Anketa.description)
    await callback.message.delete()


@user_main_router.callback_query(F.data == 'skip_report_description', StateFilter(Anketa.description))
async def handle_skip_description_button(callback: CallbackQuery, state: FSMContext):
    if callback.message.chat.type != "private" or await db_methods.user_is_muted(callback.from_user.id):
        return

    await callback.message.answer(render_template("user_answers/report_created.html"), parse_mode="HTML")

    await state.update_data(desc="Комментарий отсутсвует")

    data = await state.get_data()

    report = await db_methods.create_user_report(
        user_id=callback.message.from_user.id,
        report_floor=data['floor'],
        report_audience=data['audi'],
        report_reason=data['trouble'],
        report_description=data['desc']
    )

    await state.set_state(UserStates.global_state)

    await send_report_to_admins(report.id)


@user_main_router.message(F.text, StateFilter(Anketa.description))
async def handle_adding_report_description(message: types.Message, state: FSMContext):

    if message.chat.type != "private" or await db_methods.user_is_muted(message.from_user.id):
        return

    await message.answer(render_template("user_answers/report_created.html"), parse_mode="HTML")

    await state.update_data(desc=message.text)

    data = await state.get_data()

    report = await db_methods.create_user_report(
        user_id=message.from_user.id,
        report_floor=data['floor'],
        report_audience=data['audi'],
        report_reason=data['trouble'],
        report_description=data['desc']
    )

    await state.set_state(UserStates.global_state)

    await send_report_to_admins(report.id)
