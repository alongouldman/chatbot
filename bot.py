# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
import time
import re
import os

# get the bot token from the enviroment variable.
# note: you must add a bot token to your environment to make this bit work, and save it with the name 'BOT_TOKEN'
TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)

# def expense_parser(bot, update):
#     message = update.message.text
#     amount, category, expense = message.split(',')
#     update.message.reply_text(f'you bought {expense} (which is {category}) and it cost {amount} shekels!')

@bot.message_handler(func=lambda message: True)
def expense_parse(message):
    expense = {'amount': None,
               'expense': None,
               'category': None
               }
    user_message = message.text.split(',')

    # input validations
    # validate number of fields
    if len(user_message) < len(expense):
        bot.reply_to(message, '''missing details. you should write:
        1. how much money was spent?
        2. what did you buy?
        3. what category was it?
        you can also add comments after the expense.
        example: 
        '300 שקל, מתנה לחתונה של שלומי ושלומית, מתנות'
        please send again.''')

    # validate amount format
    # extract the value from any characters using REGEX
    amount_pattern = re.compile(r'(\b[-+]?[0-9]+\.?[0-9]*\b)')
    expense['amount'] = amount_pattern.search(user_message[0])

    # check that the amount is a valid number (can be a float)
    # in the future: list all valid categories, and check if it's simillar to a one of the categories using machean learning







@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "good morning!")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "the bot is running. in order to send detailes about your expanse, send in this format:\nhow much did you spend? comma (,), what was it about, and what category is the expanse")


print("bot started")
while True:
    try:
        bot.polling()
    except:
        time.sleep(2)

