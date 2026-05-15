import os
import json
import time
from telebot import TeleBot, types
from dotenv import load_dotenv

# 1. .env faylidan token va URL'ni yuklash
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')

# Botni ishga tushirish
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Keshni majburan yangilash uchun vaqt tamg'asidan (timestamp) foydalanamiz
    # Bu har safar Telegram-ga saytni yangidan yuklashni buyuradi
    timestamp = int(time.time())
    web_app_link = f"{WEB_APP_URL}?v={timestamp}"
    
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    # WebApp tugmasini yaratish
    web_app = types.WebAppInfo(web_app_link)
    item = types.KeyboardButton("🇬🇧 Ingliz tili testini boshlash", web_app=web_app)
    markup.add(item)
    
    welcome_text = (
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Ingliz tili darajangizni aniqlash uchun testga xush kelibsiz.\n"
        "Pastdagi tugmani bosing va o'zingizga mos darajani tanlang. ✨"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    """Web App'dan kelgan natijalarni qayta ishlash"""
    try:
        # JSON ma'lumotlarni o'qiymiz
        data = json.loads(message.web_app_data.data)
        
        level = data.get('level', 'Noma\'lum')
        score = data.get('score', 0)
        total = data.get('total', 20)
        
        # Natija uchun chiroyli xabar tayyorlash
        percentage = int((score / total) * 100)
        
        result_text = (
            f"🏁 **Test yakunlandi!**\n\n"
            f"📈 Daraja: *{level}*\n"
            f"✅ To'g'ri javoblar: *{score} ta*\n"
            f"📊 Umumiy savollar: *{total} ta*\n"
            f"🎯 Ko'rsatkich: *{percentage}%*\n\n"
        )
        
        # Natijaga qarab izoh qo'shish
        if percentage >= 80:
            result_text += "Ajoyib! Siz bu darajani juda yaxshi o'zlashtirgansiz. 🌟"
        elif percentage >= 50:
            result_text += "Yaxshi natija, lekin hali o'rganishda davom etish kerak. 👍"
        else:
            result_text += "Ko'proq shug'ullanishni tavsiya qilamiz. 💪"

        bot.send_message(message.chat.id, result_text, parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, "Natijani qayta ishlashda xatolik yuz berdi.")
        print(f"Xatolik: {e}")

if __name__ == '__main__':
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.polling(none_stop=True)