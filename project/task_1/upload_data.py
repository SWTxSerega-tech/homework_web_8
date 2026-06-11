import json
from models import Author, Quote
from mongoengine import connect
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv('MONGO_URL')

connect(db='quotes_db', host=MONGODB_URL)
print('Connected to MongoDB!')

Author.drop_collection()
Quote.drop_collection()

BASE_DIR = Path(__file__).resolve().parent

AUTHORS_PATH = BASE_DIR / 'authors.json'
QUOTES_PATH = BASE_DIR / 'quotes.json'

def upload_authors():
    with open(AUTHORS_PATH, 'r', encoding='utf-8') as f:
        authors = json.load(f)
        
    for author in authors:
        Author(
            fullname = author['fullname'],
            born_date = author['born_date'],
            born_location = author['born_location'],
            description = author['description']
        ).save()
    
    print('Authors uploaded!')
    
def upload_quotes():
    with open(QUOTES_PATH, 'r', encoding='utf-8') as f:
        quotes = json.load(f)
        
    for quote in quotes:
        
        author_doc = Author.objects(fullname = quote['author']).first()
        if author_doc:
            Quote(
                tags = quote['tags'],
                author = author_doc,
                quote = quote['quote']
            ).save()
        else:
            print(f'Author {quote["author"]} not found')
    
    print('Quotes uploaded!')
    
if __name__ == '__main__':
    upload_authors()
    upload_quotes()