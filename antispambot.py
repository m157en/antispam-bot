from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваши команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет, я ваш анти-спам бот!')

# Основная функция
def main() -> None:
    """Запуск бота."""
    # Вставьте ваш токен
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Добавляем обработчик команды /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
