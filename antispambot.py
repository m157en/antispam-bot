import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import time
import os

# Включаем логирование для отслеживания ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Создадим список для хранения сообщений пользователей
user_messages = {}

# Минимальное время между сообщениями (в секундах)
COOLDOWN_TIME = 2  # например, 2 секунды
SPAM_THRESHOLD = 5  # максимальное количество сообщений за данный интервал времени

# Функция, которая вызывается при старте бота
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я анти-спам бот. Я блокирую спам-сообщения.')

# Функция для обработки входящих сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    current_time = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    # Очищаем старые сообщения, которые старше 10 секунд
    user_messages[user_id] = [msg_time for msg_time in user_messages[user_id] if current_time - msg_time < COOLDOWN_TIME]

    # Добавляем текущее сообщение
    user_messages[user_id].append(current_time)

    # Если количество сообщений за заданный интервал превышает порог, это спам
    if len(user_messages[user_id]) > SPAM_THRESHOLD:
        await update.message.reply_text('Вы отправляете слишком много сообщений. Блокировка на 30 секунд.')
        await context.bot.kick_chat_member(update.message.chat_id, user_id)
    else:
        # Если не спам, просто отвечаем сообщением
        await update.message.reply_text('Ваше сообщение получено.')

# Функция для обработки ошибок
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Ошибка {context.error}')

# Основная асинхронная функция
async def main():
    # Введите ваш токен, который вы получили от BotFather
    token = os.getenv("TELEGRAM_TOKEN")  # Используем переменную окружения для токена

    # Создание объекта Application
    application = Application.builder().token(token).build()

    # Регистрируем обработчик команд /start
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрируем обработчик ошибок
    application.add_error_handler(error)

    # Запускаем бота
    await application.run_polling()

if __name__ == "__main__":
    # Получаем цикл событий
    loop = asyncio.get_event_loop()

    # Запускаем основную асинхронную задачу
    loop.create_task(main())
    loop.run_forever()
