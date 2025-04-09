import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update: Update, context):
    """Простой обработчик для /start"""
    await update.message.reply_text("Привет! Я антиспам-бот.")

# Основная функция
def main():
    # Получаем токен из переменных окружения
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Токен не задан в переменных окружения!")
    
    # Создаем экземпляр бота
    application = Application.builder().token(token).build()

    # Регистрируем команду /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Получаем порт из переменной окружения, если его нет - ставим по умолчанию 8080
    port = int(os.getenv("PORT", 8080))

    # Запускаем бота с поллингом
    application.run_polling()

if __name__ == "__main__":
    main()
