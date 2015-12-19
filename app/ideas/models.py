from peewee import *
from app.auth.models import User
from app.models import DATABASE


class Idea(Model):
    id = PrimaryKeyField()
    user = ForeignKeyField(User)
    title = CharField(unique=True)
    content = TextField()
    votes = IntegerField(default=0)

    class Meta:
        database = DATABASE


class IdeaVotes(Model):
    idea = ForeignKeyField(Idea)
    user = ForeignKeyField(User)

    class Meta:
        database = DATABASE