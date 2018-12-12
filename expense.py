from custom_errors import *
from utils import *


class Expense:
    def __init__(self, message):
        # input string
        user_message = message.text.split(' ')
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
            # collect all other expenses details
            self._expense_details = ''
            for i in range(2, len(user_message)):
                self._expense_details += user_message[i] + ' '
            self._expense_details.rstrip()

        # input date
        self._date = get_time(message)

    def __repr__(self):
        expense = f"amount: {self._amount}\ncategory: {self._category}"
        if self._expense_details:
            expense += f"\ndetails: {self._expense_details}"
        expense+= f"\ndate: {self._date.day}.{self._date.month}.{self._date.year}"
        return expense