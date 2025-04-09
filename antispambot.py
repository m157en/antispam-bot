import logging
import os
from flask import Flask
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import time
import threading

# Включаем логирование для отслеживания ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

# Минимальное время между сообщениями (в секундах)
COOLDOWN_TIME = 2  # например, 2 секунды
SPAM_THRESHOLD = 5  # максимальное количество сообщений за данный интервал времени

# Список для хранения сообщений пользователей
user_messages = {}

# Функция, которая вызывается при старте бота
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я анти-спам бот. Я блокирую спам-сообщения.')

# Функция для обработки входящих сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    current_time = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    # Очищаем старые сообщения, которые старше COOLDOWN_TIME
    user_messages[user_id] = [msg_time for msg_time in user_messages[user_id] if current_time - msg_time < COOLDOWN_TIME]

    # Добавляем текущее сообщение
    user_messages[user_id].append(current_time)

    # Если количество сообщений за заданный интервал превышает порог, это спам
    if len(user_messages[user_id]) > SPAM_THRESHOLD:
        update.message.reply_text('Вы отправляете слишком много сообщений. Блокировка на 30 секунд.')
        context.bot.kick_chat_member(update.message.chat_id, user_id)
    else:
        # Если не спам, просто отвечаем сообщением
        update.message.reply_text('Ваше сообщение получено.')

# Функция для обработки ошибок
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Ошибка {context.error}')

# Функция для запуска телеграм-бота
def run_telegram_bot():
    token = '7995709418:7995709418:AAEof7qpf2XCFLEV4I_J5_9pD0j7qHqdqlw'

    # Создание объекта Updater
    updater = Updater(token)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команд /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик сообщений
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрируем обработчик ошибок
    dispatcher.add_error_handler(error)

    # Запускаем бота
    updater.start_polling()

    # Работа бота продолжается до его остановки
    updater.idle()

# Запуск Flask сервера на порту, который указан в окружении Render
@app.route('/')
def index():
    return 'Анти-спам бот работает!'

# Настройка порта и хоста для Flask
if __name__ == '__main__':
    # Создаем отдельный поток для запуска бота
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()

    # Запуск Flask сервера
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
