import os
import re
from datetime import datetime
from typing import Optional

import pytz
import telegram
from pytz import timezone

# =====================================
#  global variables
# =====================================

# =====================================
#  functions
# =====================================


def extract_number(user_input) -> Optional[float]:
    """
    gets the amount of money from a string
    :param user_input: string with digits in it
    :return: the numbers from the string (as a string)
    """
    amount_pattern = re.compile(r'(\b[-+]?[0-9]+\.?[0-9]*\b)')
    number = amount_pattern.search(user_input)
    if not number:
        return None
    return float(number[0])


def get_message_date(message: telegram.message.Message) -> datetime:
    '''
    :param message: telegramAPI message object
    :return: a datetime object
    '''
    datetime = message.date.replace(tzinfo=pytz.utc)
    israel_time_zone = pytz.timezone('Israel')
    datetime = datetime.astimezone(israel_time_zone)
    return datetime


def remove_money_words(all_words):
    with open(os.path.join(os.path.dirname(__file__), 'money_words.txt'), 'r', encoding="utf-8-sig") as file:
        money_words = file.read().splitlines()
        return [item for item in all_words if item not in money_words]


def get_bot_token() -> str:
    try:
        token = os.environ['BOT_TOKEN']
    except KeyError:
        with open(os.path.join(os.path.dirname(__file__), 'bot_token.txt'), 'r') as f:
            token = f.read()
    return token.strip()
