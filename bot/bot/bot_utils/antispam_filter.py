"""
Простой фильтр на спам, не сохраняющий состояния пользователей в базе данных
"""
import time
from aiogram.types import Message

# Параметры ограничения
POST_COOLDOWN = 5          # Интервал между сообщения
WARNING_THRESHOLD = 3         # Количество предупреждений до блокировки
INITIAL_BAN_TIME = 30         # Начальная длительность блокировки в секундах
BAN_MULTIPLIER = 2            # Множитель для увеличения длительности бана

# Хранилище временных меток, предупреждений и блокировок
user_post_timestamps = {}     # Время последнего поста пользователя
user_warnings = {}            # Количество предупреждений
user_bans = {}                # Время разблокировки пользователя
user_ban_count = {}           # Количество предыдущих банов пользователя


async def anti_spam_handler(message: Message) -> bool:
    """
    Проверка на спам для отправки постов в предложку. Возвращает True, если сообщение прошло проверку,
    и False, если пользователь заблокирован или должен подождать перед следующим отправлением.
    """
    user_id = message.from_user.id
    current_time = time.time()

    # Проверяем, не заблокирован ли пользователь
    if user_id in user_bans and current_time < user_bans[user_id]:
        # Игнорируем сообщение, если пользователь в блокировке
        return False

    # Проверка времени последнего отправленного соощения
    if user_id in user_post_timestamps:
        last_post_time = user_post_timestamps[user_id]
        if current_time - last_post_time < POST_COOLDOWN:
            # Увеличиваем количество предупреждений
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

            # Если превышен порог предупреждений, блокируем пользователя
            if user_warnings[user_id] >= WARNING_THRESHOLD:
                # Увеличиваем счетчик банов
                user_ban_count[user_id] = user_ban_count.get(user_id, 0) + 1

                # Рассчитываем длительность бана на основе количества предыдущих банов
                ban_duration = INITIAL_BAN_TIME * (BAN_MULTIPLIER ** user_ban_count[user_id])

                # Устанавливаем время разблокировки и сбрасываем предупреждения
                user_bans[user_id] = current_time + ban_duration
                user_warnings[user_id] = 0  # Сбрасываем счетчик предупреждений

                await message.answer(
                    f"{message.from_user.full_name.capitalize()}, вы временно заблокированы за частые попытки отправки постов. Подождите {int(ban_duration)} секунд"
                )
            else:
                await message.answer(
                    "Не так быстро!"
                )
            return False

    # Если прошло достаточно времени, сбрасываем предупреждения и обновляем время последнего поста
    user_post_timestamps[user_id] = current_time
    user_warnings[user_id] = 0
    return True


# Очистка старых данных, использовать когда нужно
def cleanup_old_data():
    current_time = time.time()
    # Удаляем устаревшие записи из словарей
    for user_id in list(user_post_timestamps):
        if current_time - user_post_timestamps[user_id] > POST_COOLDOWN:
            del user_post_timestamps[user_id]
    for user_id in list(user_bans):
        if current_time > user_bans[user_id]:
            del user_bans[user_id]
            del user_ban_count[user_id]  # Сбрасываем счетчик банов после разблокировки
