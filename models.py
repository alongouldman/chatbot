import datetime
import os
import random

import mongoengine
import pandas
from mongoengine import connect, Document, StringField, FloatField, DateTimeField, \
    IntField, BooleanField, get_connection, EmbeddedDocumentListField, EmbeddedDocument, \
    ListField, ReferenceField
from mongoengine.queryset.visitor import Q
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
    def get_class_variables(cls):
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


class Category(Document):

    meta = {
        'collection': 'categories'
    }

    name = StringField(required=True, primary_key=True)  # most be unique
    type = StringField(required=True, choices=CategoryType.get_class_variables())  # category type

    def __str__(self):
        return f"<Category object: name={self.name}, type={self.type}>"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Category) and self.name == other.name

    @staticmethod
    @ensure_db_connection
    def init_categories():
        existing_categories = Category.objects()
        df = pandas.read_csv('scripts/initial_categories.csv')
        if not existing_categories.filter(name=CategoryType.UNKNOWN):
            unknown_category = Category(CategoryType.UNKNOWN, type=CategoryType.UNKNOWN)
            unknown_category.save()
            logging.info(f'category {unknown_category} saved')

        existing_categories_names = {cat.name for cat in existing_categories.all()}
        for index, row in df.iterrows():
            if row['name'] not in existing_categories_names:
                category = Category()
                category.name = row['name']
                category.type = row['type']

                try:
                    category.save()
                    logging.info(f'category {category} saved')
                except RuntimeError as e:
                    logging.error(e)
            else:
                logging.info(f"category {row['name']} exists")
                

class TelegramGroup(Document):
    meta = {
        'collection': 'telegram_groups'
    }

    telegram_chat_id = StringField(required=True, primary_key=True)
    user_ids = ListField(default=[])

    def __repr__(self):
        return f"<TelegramGroup object, id={self.telegram_chat_id} user_ids={self.user_ids}>"

    # def add_category(self, category: Category):
    #     exists = any([cat.name == category.name for cat in self.categories])
    #     if not exists:
    #         return self.categories.append(category)
    #     raise RuntimeError(f"category with name={category.name} already exists")


class Expense(Document):

    meta = {
        'collection': 'expenses'
    }

    date = DateTimeField(required=True)
    remember_category = BooleanField(required=True, default=True)
    description = StringField()
    amount = FloatField(required=True)
    category = ReferenceField(Category, required=True, default=Category(name=CategoryType.UNKNOWN), reverse_delete_rule=mongoengine.NULLIFY)
    telegram_group = ReferenceField(TelegramGroup, required=True, reverse_delete_rule=mongoengine.CASCADE)

    def __str__(self):
        return f"<Expense object, date: {self.date} description: {self.description} amount: {self.amount}, category_name={self.category.name}, group_id={self.telegram_group.telegram_chat_id}>"

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
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        with open('db_connection_string.txt') as f:
            connection_string = f.read()
    connect(host=connection_string, connect=False)
    Category.init_categories()
    group = TelegramGroup.objects().first()
    # group = TelegramGroup(telegram_chat_id=str(random.randint(0, 1000)))
    group.save()
    for i in range(200):
        expense = Expense(date=datetime.date.today(),
                           amount=24.32,
                           description="something")
        expense.telegram_group = group
        expense.category = random.choice(Category.objects().all())
        expense.save()
        logging.info(f'expense {expense} saved')


    # Category.objects(name='אוכל')
    # expense1.save()
    print("done")
