import os
import pathlib
from enum import Enum
from functools import lru_cache
from threading import Thread

import mongoengine
import pandas
from mongoengine import connect, Document, StringField, FloatField, DateTimeField, \
    IntField, BooleanField, get_connection, EmbeddedDocumentListField, EmbeddedDocument, \
    ListField, ReferenceField
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_db_connection(func):
    def inner(*args, **kwargs):
        try:
            get_connection()
        except mongoengine.connection.ConnectionFailure:
            logger.info("no DB connection, connecting to DB....")
            init_session()
        return func(*args, **kwargs)
    return inner


def init_session():
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        connection_string_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_connection_string.txt')
        with open(connection_string_path) as f:
            connection_string = f.read()
    connection = connect(host=connection_string)
    logger.info("DB connected")
    return connection


class StringEnum(object):
    @classmethod
    def values(cls):
        wanted_values = []
        for key, value in cls.__dict__.items():
            if not key.startswith('__'):
                wanted_values.append(value)
        return wanted_values


class CategoryType(StringEnum):
    VITAL_AND_REOCCURING = 'vital and reoccuring'
    VITAL_AND_CHANGES = 'vital and changes'
    UNNECESSARY_AND_REOCCURING = 'unnecessary and reoccuring'
    UNNECESSARY_AND_CHANGES = 'unnecessary and changes'
    INCOME = "income"
    INVESTMENT = 'investment'
    STUDY = 'study'
    UNKNOWN = 'unknown'


# # TODO: migrate investment categories in production DB.
class Category:
    def __init__(self, name, type_):
        self.name = name
        assert type_ in CategoryType.values()
        self.type = type_

    def __str__(self):
        return f"<Category object: name={self.name}, type={self.type}>"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Category) and self.name == other.name

    @classmethod
    @lru_cache(maxsize=None)
    def all_categories(cls):
        file_errors_location = pathlib.Path(__file__).parent.absolute() / 'scripts/initial_categories.xlsx'
        df = pandas.read_excel(file_errors_location)
        all_categories = []
        for index, row in df.iterrows():
            all_categories.append(cls(row['name'], row['type']))
        return all_categories


class TelegramGroup(Document):
    meta = {
        'collection': 'telegram_groups'
    }

    telegram_chat_id = StringField(required=True, primary_key=True)
    user_ids = ListField(default=[])

    def __repr__(self):
        return f"<TelegramGroup object, id={self.telegram_chat_id} user_ids={self.user_ids}>"


class Expense(Document):

    meta = {
        'collection': 'expenses'
    }

    date = DateTimeField(required=True)
    remember_category = BooleanField(required=True, default=True)
    description = StringField()
    amount = FloatField(required=True)
    category = StringField(required=True)
    telegram_group = ReferenceField(TelegramGroup, required=True, reverse_delete_rule=mongoengine.CASCADE)

    def __str__(self):
        return f"<Expense object, date: {self.date} description: {self.description} amount: {self.amount}, category={self.category}, group_id={self.telegram_group.telegram_chat_id}>"

# class BankAccount(EmbeddedDocument):
#     hashed_username
#     hashed_password
#     type
#
# class User(Document):
#     telegram_user_id
#     bank_accounts =
#     salt
#     email
#     hashed_password


if __name__ == "__main__":
    # TODO: write some tests for the object types...
    # try:
    #     connection_string = os.environ['db_connection_string']
    # except KeyError:
    #     with open('db_connection_string.txt') as f:
    #         connection_string = f.read()
    # connect(host=connection_string, connect=False)
    print(Category.all_categories())
    print(Category.all_categories())
    print(Category.all_categories())
    
    # group = TelegramGroup.objects().first()
    # group.save()
    # expense = Expense(date=datetime.date.today(),
    #                        amount=24.32,
    #                        description="something")
    # expense.telegram_group = group
    # expense.category = "test"
    # expense.save()
    # logging.info(f'expense {expense} saved')

    print("done")
