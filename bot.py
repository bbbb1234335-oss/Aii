from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = model.generate_content(user_text)

    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot Running...")
app.run_polling()
