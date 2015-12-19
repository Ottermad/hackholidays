from peewee import *
from app.models import DATABASE
from flask.ext.bcrypt import generate_password_hash


class User(Model):
    user_id = PrimaryKeyField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def add_user(cls, email, password):
        User.create(
            email=email,
            password=generate_password_hash(password)
        )