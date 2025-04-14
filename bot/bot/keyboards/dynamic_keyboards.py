from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def show_report_by_id(report_id: int):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Просмотреть репорт", callback_data=f"show_report_by_id_{report_id}")
    return keyboard_builder.as_markup()


def mute_user_by_id(user_id: int):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Заблокировать пользователя", callback_data=f"mute_user_by_id_{user_id}")
    return keyboard_builder.as_markup()
