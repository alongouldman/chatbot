import datetime
import os
from mongoengine import connect, Document, StringField, DynamicDocument, FloatField, DateTimeField, ReferenceField, \
    IntField, BooleanField, get_connection, MongoEngineConnectionError, EmbeddedDocumentListField, EmbeddedDocument
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


class ExpenseType(StringEnum):
    CREDIT = 'credit'
    DEBIT = 'debit'


class Expense(EmbeddedDocument):

    meta = {
        'collection': 'expenses'
    }

    date = DateTimeField(required=True)
    # TODO: should I do that?
    # category = ReferenceField(Category, required=True, default=CategoryType.UNKNOWN)
    remember_category = BooleanField(required=True, default=True)
    description = StringField()
    amount = FloatField(required=True)
    type = StringField(required=True, default=ExpenseType.DEBIT, choices=ExpenseType.get_class_variables())  # credit or debit

    def __str__(self):
        return f"date: {self.date} description: {self.description} amount: {self.amount} type: {self.type}"


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

    name = StringField(required=True)
    type = StringField(required=True, choices=CategoryType.get_class_variables())  # category type
    expenses = EmbeddedDocumentListField(Expense, default=[])

    def __str__(self):
        return f"id={self.id}, name={self.name}, type={self.type}"

    def exists(self):
        if Category.objects(Q(name=self.name) & Q(type=self.type)):
            return True
        return False


if __name__ == "__main__":
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        with open('db_connection_string.txt') as f:
            connection_string = f.read()
    connect(host=connection_string, connect=False)
    print("DB is conected")

    cat1 = Category('אוכל', type=CategoryType.VITAL_AND_CHANGES)
    cat2 = Category('ביגוד', type=CategoryType.VITAL_AND_CHANGES)
    cat3 = Category('תחבורה', type=CategoryType.VITAL_AND_CHANGES)
    cat4 = Category(CategoryType.UNKNOWN, type=CategoryType.UNKNOWN)
    cat1.save()
    cat2.save()
    cat3.save()
    cat4.save()

    expense1 = Expense(date=datetime.date.today(),
                       amount=24.32,
                       description="something"
                       )

    Category.objects(name='אוכל')
    expense1.save()
    print("done")
