from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .subject import Subject

class Score(Model):
    user = ForeignKeyField(User, backref='scores')
    product = ForeignKeyField(Product, backref='scores')
    score_date = DateTimeField()

    class Meta:
        database = db
