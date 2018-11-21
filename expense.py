from custom_errors import *
from utils import *


class Expense:
    def __init__(self, message):
        user_message = message.split(',')

        # input validations
        self._amount = get_amount(user_message[0])
        if not self._amount:
            raise NoAmountError
        if len(user_message) == 1:  # only amount, without category
                raise NoCategoryError
        # TODO: in the future: list all valid categories, and check if it's simillar to a one of the categories using machean learning
        self._category = user_message[1]
        if len(user_message) == 2:  # assume the user sent amount and category, without expanse details
            self._expense_details = None
        else:
            self._expense_details = user_message[2]

        if len(user_message) < len(expense):
            bot.reply_to(message, '''missing details. you should write:
            1. how much money was spent?
            2. what did you buy?
            3. what category was it?
            you can also add comments after the expense.
            example: 
            '300 שקל, מתנה לחתונה של שלומי ושלומית, מתנות'
            please send again.''')


