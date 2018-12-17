import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json


def get_credentials(scope):
    keyfile_dict = json.loads(os.environ['BOT_GOOGLE_SECRET'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)
    return creds


def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = get_credentials(scope)
    client = gspread.authorize(creds)

    spread_sheet = client.open('outcomes from telegram bot')
    work_sheet = spread_sheet.sheet1
    # results = sheet.get_all_records()
    # return results
    return work_sheet


def add_to_sheet(expense):
    work_sheet = get_worksheet()
    # date = ".".join([expense.date.day, expense.date.month, expense.date.year])
    date = f"{expense.date:%d.%m.%Y}"
    new_row = [date, expense.amount, expense.category]
    if expense.expense_details:
        new_row.append(expense.expense_details)
    work_sheet.append_row(new_row)


