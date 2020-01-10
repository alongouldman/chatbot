import datetime
import os
import random

import pandas
from mongoengine import connect, Document, StringField, FloatField, DateTimeField, \
    IntField, BooleanField, get_connection, MongoEngineConnectionError, EmbeddedDocumentListField, EmbeddedDocument, \
    ListField
from mongoengine.queryset.visitor import Q
import logging


# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_db_connection(func):
    def inner(*args, **kwargs):
        try:
            get_connection()
        except MongoEngineConnectionError:
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
    def get_class_variables(cls):
        wanted_values = []
        for key, value in cls.__dict__.items():
            if not key.startswith('__'):
                wanted_values.append(value)
        return wanted_values


class Expense(EmbeddedDocument):

    meta = {
        'collection': 'expenses'
    }

    date = DateTimeField(required=True)
    remember_category = BooleanField(required=True, default=True)
    description = StringField()
    amount = FloatField(required=True)

    def __str__(self):
        return f"<Expense object, date: {self.date} description: {self.description} amount: {self.amount}>"


class CategoryType(StringEnum):
    VITAL_AND_REOCCURING = 'vital and reoccuring'
    VITAL_AND_CHANGES = 'vital and changes'
    UNNECESSARY_AND_REOCCURING = 'unnecessary and reoccuring'
    UNNECESSARY_AND_CHANGES = 'unnecessary and changes'
    INCOME = "income"
    INVESTMENT = 'investment'
    STUDY = 'study'
    UNKNOWN = 'unknown'


class Category(EmbeddedDocument):

    meta = {
        'collection': 'categories'
    }

    name = StringField(required=True)  # most be unique
    type = StringField(required=True, choices=CategoryType.get_class_variables())  # category type
    expenses = EmbeddedDocumentListField(Expense, default=[])

    def __str__(self):
        return f"<Category object: name={self.name}, type={self.type}>"

    def __repr__(self):
        return self.__str__()


class TelegramGroup(Document):
    meta = {
        'collection': 'telegram_groups'
    }

    telegram_chat_id = StringField(required=True, unique=True)
    categories = EmbeddedDocumentListField(Category, default=[])
    user_ids = ListField(default=[])

    def init_categories(self):
        df = pandas.read_csv('scripts/initial_categories.csv')
        unknown_category = Category(CategoryType.UNKNOWN, type=CategoryType.UNKNOWN)
        self.add_category(unknown_category)

        for index, row in df.iterrows():
            category = Category()
            category.name = row['name']
            category.type = row['type']

            try:
                self.add_category(category)
                logging.info(f'category {category} saved')
            except RuntimeError as e:
                logging.error(e)

    def __repr__(self):
        return f"<TelegramGroup object, id={self.telegram_chat_id} user_ids={self.user_ids}>"

    def add_category(self, category: Category):
        exists = any([cat.name == category.name for cat in self.categories])
        if not exists:
            return self.categories.append(category)
        raise RuntimeError(f"category with name={category.name} already exists")


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
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        with open('db_connection_string.txt') as f:
            connection_string = f.read()
    connect(host=connection_string, connect=False)
    print("DB is conected")
    expense1 = Expense(date=datetime.date.today(),
                       amount=24.32,
                       description="something"
                       )

    cat1 = Category('אוכל', type=CategoryType.VITAL_AND_CHANGES, expenses=[expense1])
    cat2 = Category('אוכל', type=CategoryType.VITAL_AND_CHANGES)
    cat3 = Category('תחבורה', type=CategoryType.VITAL_AND_CHANGES)
    cat4 = Category(CategoryType.UNKNOWN, type=CategoryType.UNKNOWN)
    group = TelegramGroup(telegram_chat_id=str(random.randint(0, 1000)))
    group.init_categories()
    group.save()
    group.add_category(cat1)
    group.add_category(cat2)
    group.add_category(cat1)
    group.add_category(cat1)
    group.save()

    # Category.objects(name='אוכל')
    # expense1.save()
    print("done")
