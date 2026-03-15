from flask import Flask, request
import asyncio
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -5239091049


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )


application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.ALL, forward_message))


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if update:
        asyncio.run(
            application.process_update(
                Update.de_json(update, application.bot)
            )
        )

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
