import json
from models import Author, Quote
from mongoengine import connect
from bson import ObjectId
from dotenv import load_dotenv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

MONGODB_URL = os.getenv('MONGO_URL')

connect(db='quotes_db', host=MONGODB_URL)
print('Connected to MongoDB!')

steve_martin = ObjectId('6a2b188d9e5f64650205378e')
alber_einshtein = ObjectId('6a2b188d9e5f64650205378d')

                            
def search_by_author(author_name):
    if author_name == 'Steve Martin':
        quotes = Quote.objects(author=steve_martin)
        
        for q in quotes:
            print(q.quote)
            
    elif author_name == 'Albert Einstein':
        quotes = Quote.objects(author=alber_einshtein)
        
        for q in quotes:
            print(q.quote)
            

def search_by_tag(tag_name):
    if tag_name:
        quotes = Quote.objects(tags=tag_name)
        
        for q in quotes:
            print(q.quote)        
            

def search_by_tags(tags_string):
    if tags_string:
        
        tags_list = [tag.strip() for tag in tags_string.split(',')]
        
        quotes = Quote.objects(tags__all=tags_list)
        
        for q in quotes:
            print(q.quote)

def main():
    print("Скрипт пошуку цитат запущено. Доступні команди: name:, tag:, tags:, exit")
    
    while True:
        # Отримуємо введення від користувача та прибираємо зайві пробіли з кінців
        user_input = input("\nВведіть команду: ").strip()
        
        # Перевірка на вихід
        if user_input.lower() == 'exit':
            print("Завершення роботи скрипту. До побачення!")
            break
            
        # Перевіряємо, чи є двокрапка у введенні
        if ':' not in user_input:
            print("Помилка: Неправильний формат. Використовуйте формат 'команда: значення'.")
            continue
            
        # Розділяємо команду та значення (максимум 1 розділення)
        command, value = user_input.split(':', 1)
        command = command.strip().lower()
        value = value.strip()
        
        # Перевірка на порожнє значення
        if not value:
            print("Помилка: Значення команди не може бути порожнім.")
            continue
            
        # Виклик відповідної логіки залежно від команди
        if command == 'name':
            search_by_author(value)
        
        elif command == 'tag':
            search_by_tag(value)
        
        elif command == 'tags':
            search_by_tags(value)
        
        else:
            print(f"Помилка: Невідома команда '{command}'. Доступні: name, tag, tags, exit")

if __name__ == "__main__":
    main()

            
        
