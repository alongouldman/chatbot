import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from custom_errors import *


def get_credentials(scope):
    keyfile_dict = json.loads(os.environ['BOT_GOOGLE_SECRET'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)
    return creds


def get_spreadsheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = get_credentials(scope)
    client = gspread.authorize(creds)

    spread_sheet = client.open('outcomes from telegram bot')
    # work_sheet = spread_sheet.sheet1
    # results = sheet.get_all_records()
    # return results
    return spread_sheet


def add_to_sheet(expense):
    spread_sheet = get_spreadsheet()
    sheet_name = f"{expense.date:%m.%y}"
    # write to sheet according to the month
    try:
        work_sheet = spread_sheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # create worksheet
        work_sheet = spread_sheet.add_worksheet(sheet_name, 1, 1000)
        work_sheet.insert_row(['date', 'amount', 'category', 'details'])  # add headers
        work_sheet.resize(1)

    # date = ".".join([expense.date.day, expense.date.month, expense.date.year])
    date = f"{expense.date:%d.%m.%Y}"
    new_row = [date, expense.amount, expense.category]
    if expense.expense_details:
        new_row.append(expense.expense_details)
    work_sheet.append_row(new_row)


def pop():
    work_sheet = get_spreadsheet().worksheets()[-1]  # delete from last worksheet
    length = len(work_sheet.col_values(1))
    if length < 2:  # no rows!
        raise NoRowsError
    row_to_delete = work_sheet.row_values(length)
    # delete
    work_sheet.delete_row(length)
    return row_to_delete




