# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
import time

from bot_utils import get_bot_token
from custom_errors import NoRowsError, NoCategoryError, NoAmountError
from expense import Expense
from spreadsheet import pop, add_to_sheet


bot = telebot.TeleBot(get_bot_token())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "good morning!")


@bot.message_handler(commands=['delete'])
def delete_last(message):
    try:
        deleted = pop()
    except NoRowsError:
        bot.reply_to(message, 'no rows to delete')
    else:
        msg = "DELETED:"
        for cell in deleted:
            msg += "\n" + cell
        bot.reply_to(message, msg)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "the bot is running. in order to send detailes about your expanse, send in this format:\nhow much did you spend? comma (,), what was it about, and what category is the expanse")
    # TODO: make this help function better


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
        try:
            add_to_sheet(expense)
        except Exception as err:
            if hasattr(err, 'message'):
                bot.reply_to(message, err.message)
            else:
                bot.reply_to(message, err)
            bot.reply_to(message, 'expense not added from some reason, sorry....\n#not_added')


if __name__ == "__main__":
    print("bot started")
    while True:
        try:
            bot.polling()
        except:
            time.sleep(2)

