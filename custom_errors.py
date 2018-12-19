class NoAmountError(Exception):
    pass


class NoCategoryError(Exception):
    pass


def unknown_error(err, bot, message):
    if hasattr(err, 'message'):
        bot.reply_to(message, err.message)
    else:
        bot.reply_to(message, err)
