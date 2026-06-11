from mongoengine import Document, StringField, ListField, ReferenceField

class Author(Document):
    meta = {'collection': 'authors'}
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    
class Quote(Document):
    meta = {'collection': 'quotes'}
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=2)
    quote = StringField(required=True)