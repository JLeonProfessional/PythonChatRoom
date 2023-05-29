from mongoengine import *


class User(Document):
    username = StringField(max_length=200, required=True)
    password = StringField(max_length=200, required=True)
    nickname = StringField(max_length=200, required=False)


def create_user(username, password):
    user = User(username=username)
    user.password = password
    user.save()

