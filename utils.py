import re


def get_amount(user_input):
    amount_pattern = re.compile(r'(\b[-+]?[0-9]+\.?[0-9]*\b)')
    number = amount_pattern.search(user_input)
    if not number:
        return None
    return number[0]


