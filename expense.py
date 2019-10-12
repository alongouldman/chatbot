from custom_errors import NoAmountError, NoCategoryError
from utils import remove_money_words, get_amount, get_time


class Expense:
    def __init__(self, message):
        # input string
        user_message = message.text.split(' ')
        # input validations
        user_message = remove_money_words(user_message)  # removing "money words"

        self.amount = get_amount(user_message[0])
        if not self.amount:
            raise NoAmountError
        if len(user_message) == 1:  # only amount, without category
                raise NoCategoryError
        # TODO: in the future: list all valid categories, and check if it's simillar to a one of the categories using machean learning
        self.category = user_message[1]
        if len(user_message) == 2:  # assume the user sent amount and category, without expanse details
            self.expense_details = None
        else:
            # collect all other expenses details
            self.expense_details = ''
            for i in range(2, len(user_message)):
                self.expense_details += user_message[i] + ' '
            self.expense_details.rstrip()

        # input date
        self.date = get_time(message)

    def __repr__(self):
        expense = f"amount: {self.amount}\ncategory: {self.category}"
        if self.expense_details:
            expense += f"\ndetails: {self.expense_details}"
        expense+= f"\ndate: {self.date.day}.{self.date.month}.{self.date.year}"
        return expense
