# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
import time
import os
from custom_errors import *
from expense import Expense
from spreadsheet import get_records


# get the bot token from the enviroment variable.
# note: you must add a bot token to your environment to make this bit work, and save it with the name 'BOT_TOKEN'
TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['sheet'])
def google_sheets(message):
    records = get_records()
    bot.reply_to(message, records)


@bot.message_handler(commands=['test'])
def google_sheets(message):
    records = get_environ()
    bot.reply_to(message, records)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "good morning!")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "the bot is running. in order to send detailes about your expanse, send in this format:\nhow much did you spend? comma (,), what was it about, and what category is the expanse")


@bot.message_handler(func=lambda message: True)
def expense_parse(message):
    try:
        expense = Expense(message)
    except NoCategoryError:
        bot.reply_to(message, '''
            חסרים פרטים. על מה ההוצאה?
            ''')
    except NoAmountError:
        bot.reply_to(message, '''
            חסר סכום. כמה כסף בזבזת?
            ''')
    else:
        bot.reply_to(message, expense)


print("bot started")
while True:
    try:
        bot.polling()
    except:
        time.sleep(2)

