import datetime
import os
import time
from contextlib import contextmanager

from mongoengine import connect, Document, StringField, DynamicDocument, FloatField, DateTimeField, ReferenceField, \
    IntField, BooleanField


@contextmanager
def session():
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        connection_string_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_connection_string.txt')
        with open(connection_string_path) as f:
            connection_string = f.read()
    yield connect(host=connection_string)


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

    name = StringField(required=True, primary_key=True)
    type = StringField(required=True, choices=CategoryType.get_class_variables())  # category type

    def __str__(self):
        return f"<Category object at {id(self)}, name={self.name}, type={self.type}>"


class ExpenseType(StringEnum):
    CREDIT = 'credit'
    DEBIT = 'debit'
    

class Expense(DynamicDocument):

    meta = {
        'collection': 'expenses'
    }

    date = DateTimeField(required=True)
    category = ReferenceField(Category, required=True, default=CategoryType.UNKNOWN)
    remember_category = BooleanField(required=True, default=True)
    description = StringField()
    amount = FloatField(required=True)
    type = StringField(required=True, default=ExpenseType.DEBIT, choices=ExpenseType.get_class_variables())  # credit or debit

    def __str__(self):
        return f"date: {self.date}, category: {self.category}, description: {self.description}, amount: {self.amount}, type: {self.type}"


class UserGroup(Document):
    pass


if __name__ == "__main__":
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        with open('db_connection_string.txt') as f:
            connection_string = f.read()
    connect(host=connection_string, connect=False)

    # TODO: mechanizem for connectin to db
    # TODO: add all initial categories from csv
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
                       category=cat1,
                       description="something"
                       )
    expense1.save()
    print("done")
