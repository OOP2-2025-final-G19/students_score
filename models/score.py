from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .subject import Subject

class Score(Model):
    user = ForeignKeyField(User, backref='scores')
    subject = ForeignKeyField(Subject, backref='scores')
    score_date = DateTimeField()

    class Meta:
        database = db
