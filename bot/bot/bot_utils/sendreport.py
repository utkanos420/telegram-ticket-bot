"""
Передача полученного запроса от пользователя к администратора, используя объект бота, чтобы писать напрямую
"""
from loader import bot

from loguru import logger

from configs.config import admin_ids

from keyboards.dynamic_keyboards import show_report_by_id

from templates.template_engine import render_template


logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<level>[{time:YYYY-MM-DD HH:mm:ss}] #{level:<8} {file.name}:"
           "{line} - {name} - {message}</level>",
    level="DEBUG",
    colorize=True
)


async def send_report_to_admins(report_id: int):
    for admin in admin_ids:
        await bot.send_message(text=f"Получен репорт №{report_id}", reply_markup=show_report_by_id(report_id), chat_id=admin)


async def notice_muted_user(user_id: int):
    await bot.send_message(render_template("mute-notice.html"), parse_mode="HTML", chat_id=user_id)
