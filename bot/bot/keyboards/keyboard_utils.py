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


def floor_3_audiences():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="303", callback_data="audience_303")
    keyboard_builder.button(text="305", callback_data="audience_305")
    keyboard_builder.button(text="308", callback_data="audience_308")
    keyboard_builder.button(text="312a", callback_data="audience_312a")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def floor_4_audiences():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="400", callback_data="audience_400")
    keyboard_builder.button(text="402", callback_data="audience_402")
    keyboard_builder.button(text="403", callback_data="audience_403")
    keyboard_builder.button(text="406", callback_data="audience_406")
    keyboard_builder.button(text="407", callback_data="audience_407")
    keyboard_builder.button(text="408", callback_data="audience_408")
    keyboard_builder.button(text="409", callback_data="audience_409")
    keyboard_builder.button(text="410", callback_data="audience_410")
    keyboard_builder.button(text="411", callback_data="audience_411")
    keyboard_builder.button(text="412", callback_data="audience_412")
    keyboard_builder.button(text="414", callback_data="audience_414")
    keyboard_builder.button(text="416", callback_data="audience_416")
    keyboard_builder.button(text="417", callback_data="audience_417")
    keyboard_builder.button(text="420", callback_data="audience_420")

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def floor_5_audiences():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="504", callback_data="audience_504")
    keyboard_builder.button(text="505", callback_data="audience_505")
    keyboard_builder.button(text="506", callback_data="audience_506")
    keyboard_builder.button(text="508", callback_data="audience_508")
    keyboard_builder.button(text="512", callback_data="audience_512")
    keyboard_builder.button(text="516", callback_data="audience_516")
    keyboard_builder.button(text="518", callback_data="audience_518")

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def reason_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="звук", callback_data="sound")
    keyboard_builder.button(text="проектор", callback_data="projector")
    keyboard_builder.button(text="пк", callback_data="pc")
    keyboard_builder.button(text="другое", callback_data="other")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
