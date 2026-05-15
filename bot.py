import os
from telebot import TeleBot
from dotenv import load_dotenv

# 1. .env faylini yuklaymiz
load_dotenv()

# 2. Tokenlarni o'zgaruvchilarga olamiz
TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')

# 3. Botni ishga tushiramiz
bot = TeleBot(TOKEN)

# Endi WEB_APP_URL dan bemalol foydalansangiz bo'ladi
print(f"Bot ishga tushdi. Web App URL: {WEB_APP_URL}")