import os
import json
import random
import string
from telebot import TeleBot, types
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklash
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')

bot = TeleBot(TOKEN)

# Tasodifiy matn yaratish funksiyasi (Keshni tozalash uchun)
def get_random_string(length=6):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@bot.message_handler(commands=['start'])
def start(message):
    # Har safar yangi WebAppInfo yaratamiz
    # Link oxiriga ?v=... qo'shish eski sarlavha va savollarni o'chirib tashlaydi
    cache_cleaner = get_random_string()
    web_app_link = f"{WEB_APP_URL}?v={cache_cleaner}"
    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    web_app = types.WebAppInfo(web_app_link)
    
    item = types.KeyboardButton("🇬🇧 Ingliz tili testini boshlash", web_app=web_app)
    markup.add(item)
    
    welcome_text = (
        f"Salom {message.from_user.first_name}!\n\n"
        "Ingliz tili darajangizni aniqlash uchun testni boshlang.\n"
        "Omad tilaymiz! 🚀"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_result(message):
    try:
        # Web App'dan kelgan natijani o'qish
        data = json.loads(message.web_app_data.data)
        score = data.get('score', 0)
        total = data.get('total', 20)
        
        # Natijani hisoblash
        percentage = int((score / total) * 100)
        
        result_msg = (
            "🏁 **Test yakunlandi!**\n\n"
            f"✅ To'g'ri javoblar: {score}\n"
            f"📊 Umumiy savollar: {total}\n"
            f"📈 Natija: {percentage}%\n\n"
        )
        
        if percentage >= 80:
            result_msg += "Ajoyib natija! Sizning darajangiz yuqori. 🌟"
        elif percentage >= 50:
            result_msg += "Yaxshi, lekin hali o'rganishingiz kerak bo'lgan narsalar bor. 👍"
        else:
            result_msg += "Ko'proq shug'ullanishni tavsiya qilamiz. 💪"

        bot.send_message(message.chat.id, result_msg, parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, "Natijani hisoblashda xatolik yuz berdi.")
        print(f"Error: {e}")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)