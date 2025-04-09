import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import CommandHandler, Dispatcher, Updater
from telegram.ext import CallbackContext

# Загружаем переменные окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализируем Flask-приложение
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я антиспам-бот.")

# Функция для установки webhook
def set_webhook():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Обработчик команды /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Устанавливаем webhook на ваш URL
    webhook_url = f"https://{os.getenv('RENDER_URL')}/webhook"
    updater.bot.setWebhook(webhook_url)

# Эндпоинт для webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, updater.bot)
    dispatcher = Dispatcher(updater.bot, None, workers=0)
    dispatcher.process_update(update)
    return 'ok'

# Главная функция
if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
