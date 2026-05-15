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
    # URL oxiriga ?v=1 qo'shish keshni tozalashga yordam beradi
    web_app = types.WebAppInfo(f"{WEB_APP_URL}?v={os.urandom(4).hex()}")
    item = types.KeyboardButton("🇬🇧 Ingliz tili testini boshlash", web_app=web_app)
    markup.add(item)
    
    bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! Testga tayyormisiz?", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_result(message):
    data = json.loads(message.web_app_data.data)
    score = data.get('score')
    total = data.get('total')
    
    msg = f"🏁 **Test yakunlandi!**\n\n✅ To'g'ri javoblar: {score}\n📊 Umumiy savollar: {total}\n📈 Natija: {int((score/total)*100)}%"
    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

if __name__ == '__main__':
    bot.polling(none_stop=True)