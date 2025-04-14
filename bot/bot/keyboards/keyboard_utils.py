from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def create_report_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Оставить заявку", callback_data="create_report")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def skip_report_description():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Пропустить шаг", callback_data="skip_report_description")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def floors_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="3", callback_data="floor_3")
    keyboard_builder.button(text="4", callback_data="floor_4")
    keyboard_builder.button(text="5", callback_data="floor_5")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def audi_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="405", callback_data="aud_405")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def reason_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="звук", callback_data="sound")
    keyboard_builder.button(text="проектор", callback_data="projector")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
