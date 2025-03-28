from mongoengine import Document, ListField, StringField


class Client(Document):
    email = StringField(required=True, unique=True)
    name = StringField(required=True)
    favorites = ListField(StringField())
