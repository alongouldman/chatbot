import datetime
import os
import time

from mongoengine import connect, Document, StringField, DynamicDocument, FloatField, DateTimeField, ReferenceField, \
    IntField


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


class Category(Document):

    meta = {
        'collection': 'categories'
    }

    name = StringField(required=True, primary_key=True)
    type = StringField(required=True, choices=CategoryType.get_class_variables())  # category type


class ExpenseType(StringEnum):
    CREDIT = 'credit'
    DEBIT = 'debit'
    

class Expense(DynamicDocument):

    meta = {
        'collection': 'expenses'
    }

    date = DateTimeField(required=True)
    category = ReferenceField(Category, required=True)
    description = StringField()
    amount = FloatField(required=True)
    type = StringField(required=True, default=ExpenseType.DEBIT, choices=ExpenseType.get_class_variables())  # credit or debit


class UserGroup(Document):
    pass


if __name__ == "__main__":
    try:
        connection_string = os.environ['db_connection_string']
    except KeyError:
        with open('db_connection_string.txt') as f:
            connection_string = f.read()
    connect(host=connection_string, connect=False)
    expense = Expense()
    expense.date = datetime.date.today()
    expense.amount = 45.54
    cat = Category("food", type="hi")
    cat2 = Category("food", type=CategoryType.UNNECESSARY_AND_REOCCURING)
    cat3 = Category("food", type=CategoryType.VITAL_AND_CHANGES)
    expense.category = cat
    expense.description = "we bouthg food"
    expense.save()
    cat.save()
    cat2.save()
    cat3.save()
    print("done")
