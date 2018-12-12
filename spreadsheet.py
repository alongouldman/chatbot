import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json


def get_environ():
    return os.environ['BOT_GOOGLE_SECRET']



def get_credentials(scope):
    keyfile_dict = json.loads(os.environ['BOT_GOOGLE_SECRET'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict,scope)
    return creds


def get_records():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = get_credentials(scope)
    client = gspread.authorize(creds)

    sheet = client.open('outcomes from telegram bot').sheet1

    results = sheet.get_all_records()
    return results
