import os
import json
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    web_app = types.WebAppInfo(WEB_APP_URL)
    item = types.KeyboardButton("🇬🇧 English Testni boshlash", web_app=web_app)
    markup.add(item)
    
    bot.send_message(message.chat.id, "Salom! Ingliz tili darajangizni tekshirib ko'ramizmi?", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_data(message):
    data = json.loads(message.web_app_data.data)
    score = data.get('score')
    total = data.get('total')
    
    text = (
        f"📊 **Sizning natijangiz:**\n\n"
        f"✅ To'g'ri javoblar: {score} ta\n"
        f"📝 Umumiy savollar: {total} ta\n"
        f"🎯 Foiz: {int((score/total)*100)}%"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

if __name__ == '__main__':
    print("Bot yoqildi...")
    bot.polling(none_stop=True)