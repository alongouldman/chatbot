import os

from mongoengine import connect, Document, StringField, DynamicDocument


class Expense(DynamicDocument):
    pass


class Category(Document):
    pass


class UserGroup(Document):
    pass




try:
    connection_string = os.environ['db_connection_string']
except KeyError:
    with open('db_connection_string.txt') as f:
        connection_string = f.read()
connect(host=connection_string, connect=False)
