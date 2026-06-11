from mongoengine import connect, Document, StringField, BooleanField

connect(db="email_campaign", host="mongodb://localhost:27017")

class Contact(Document):
    fullname = StringField(required=True, max_length=150)
    email = StringField(required=True, unique=True)
    is_sent = BooleanField(default=False) 
    
    phone = StringField(max_length=50)
    subject = StringField(max_length=200)

    meta = {'collection': 'contacts'}
