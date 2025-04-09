import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler
from telegram.ext import CallbackContext

# Установим логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция обработки команды /start
def start(update: Update, context: CallbackContext):
    """Отправляет приветственное сообщение пользователю"""
    update.message.reply_text("Привет! Я антиспам-бот.")

# Основная функция для запуска бота
def main():
    # Получаем токен из переменной окружения
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        raise ValueError("Токен не был найден в переменных окружения!")
    
    # Создаем объект Application с переданным токеном
    application = Application.builder().token(token).build()

    # Регистрируем команду /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Получаем порт из переменной окружения или ставим дефолтный
    port = int(os.getenv("PORT", 8080))
    
    # Запускаем бота с поллингом (без listen, Render будет сам управлять этим)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
