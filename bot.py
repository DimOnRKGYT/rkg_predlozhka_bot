from flask import Flask
import os
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -5239091049  # ID модераторской группы

# Асинхронная функция пересылки сообщений
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

# Создаем приложение Telegram
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.ALL, forward_message))

# Мини-сервер для Render, чтобы видеть порт и держать сервис alive
class Handler:
    def __init__(self, port):
        self.port = port

    def run(self):
        from http.server import HTTPServer, BaseHTTPRequestHandler

        class SimpleHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Bot is running")

        server = HTTPServer(("0.0.0.0", self.port), SimpleHandler)
        server.serve_forever()

# Функция запуска polling
def run_bot():
    application.run_polling()

# Запуск мини-сервера и бота параллельно
port = int(os.environ.get("PORT", 10000))
threading.Thread(target=Handler(port).run).start()
run_bot()
