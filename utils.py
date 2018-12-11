import re
from datetime import datetime
from pytz import timezone

# =====================================
#  global variables
# =====================================

# MONEY_WORDS = [
#     "שקל",
#     'ש"ח',
#     "שח",
#     "שקלים",
#     "שרל",
#     "\u20AA"
# ]

# =====================================
#  functions
# =====================================
def get_amount(user_input):
    '''
    gets the amount of money from a string
    :param user_input: string with digits in it
    :return: the numbers from the string (as a string)
    '''
    amount_pattern = re.compile(r'(\b[-+]?[0-9]+\.?[0-9]*\b)')
    number = amount_pattern.search(user_input)
    if not number:
        return None
    return number[0]


def get_time(message):
    '''
    :param message: telegramAPI message object
    :return: a datetime object
    '''
    unix_time = int(message.date)
    date = datetime.fromtimestamp(unix_time , timezone('Israel'))
    return date


def get_money_words():
    with open('money_words.txt', 'r') as file:
        words = file.read().splitlines()
        return words