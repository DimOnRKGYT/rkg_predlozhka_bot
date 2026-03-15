import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = -5239091049

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await context.bot.forward_message(
            chat_id=ADMIN_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

app = ApplicationBuilder().token(TOKEN).build()

handler = MessageHandler(filters.ALL, forward_message)
app.add_handler(handler)

app.run_polling()