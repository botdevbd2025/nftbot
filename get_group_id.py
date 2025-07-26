import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the group ID when someone sends a message"""
    chat_id = update.message.chat.id
    chat_type = update.message.chat.type
    chat_title = update.message.chat.title or "Private Chat"
    
    await update.message.reply_text(
        f"📋 <b>Chat Information:</b>\n\n"
        f"🆔 <b>Chat ID:</b> <code>{chat_id}</code>\n"
        f"📝 <b>Chat Type:</b> {chat_type}\n"
        f"📛 <b>Chat Title:</b> {chat_title}\n\n"
        f"💡 <b>For your .env file:</b>\n"
        f"<code>GROUP_ID={chat_id}</code>",
        parse_mode='HTML'
    )

# Create app and add handler
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, get_group_id))

print("🤖 Group ID Bot running...")
print("💡 Send any message in your group to get the group ID")

# Start the bot
app.run_polling(drop_pending_updates=True) 