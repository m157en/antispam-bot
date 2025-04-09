from flask import Flask
import threading
from telegram.ext import Application, MessageHandler, filters

TOKEN = '7873382190:AAH48KXaEfURUMGlsvwn_K1FTxIgxIntRSI'

app = Flask(__name__)

def start_bot():
    application = Application.builder().token(TOKEN).build()

    async def handle_message(update, context):
        await update.message.reply_text("Привет! Я антиспам-бот!")

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=8080)
