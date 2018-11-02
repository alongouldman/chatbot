from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def convert2upper(bot, update):
    update.message.reply_text(update.message.text.upper())
    # print(update.message.from_user.first_name)


def expense_parser(bot, update):
    message = update.message.text
    amount, category, expense = message.split(',')
    update.message.reply_text(f'you bought {expense} (which is {category}) and it cost {amount} shekels!')


def start(bot, update):
    update.message.reply_text("I'm a bot, Nice to meet you!")


def money(bot, update):
    update.message.reply_text("hi")


def main():
    updater = Updater("695592773:AAER3_OWgiKSvDP5NYf2sSmM71Iflg6GTQg")
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    money_handler = CommandHandler('money', money)
    # upper_case = MessageHandler(Filters.text, convert2upper)
    expense = MessageHandler(Filters.text, expense_parser)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(money_handler)
    dispatcher.add_handler(expense)
    # dispatcher.add_handler(upper_case)

    print("bot started")

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()


