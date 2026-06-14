import json
import os
import sys
from dotenv import load_dotenv
from mongoengine import connect
import redis  # Подключаем Redis
from models import Author, Quote

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

MONGODB_URL = os.getenv('MONGO_URL')
connect(db='quotes_db', host=MONGODB_URL)
print('Connected to MongoDB!')

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
try:
    redis_client.ping()
    print('Connected to Redis!')
except redis.ConnectionError:
    print('Warning: Redis is not running. Script will fail on cache operations.')

CACHE_TTL = 3600


def search_by_author(author_query):

    query_clean = author_query.strip().lower()
    cache_key = f"cache:name:{query_clean}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"[Redis Cache HIT] Дані загружені з кешу для '{author_query}':")
        quotes_list = json.loads(cached_data)
        if not quotes_list:
            print(f"Цитати автора {author_query} не знайдені.")
            return
        for q in quotes_list:
            print(f'\t— {q}')
        return

    
    authors = Author.objects(fullname__istartswith=query_clean)
    
    if not authors:
        print(f"Автор '{author_query}', не знайдено в базі даних.")
        redis_client.setex(cache_key, 60, json.dumps([]))
        return


    all_quotes = []
    for author in authors:
        quotes = Quote.objects(author=author)
        for q in quotes:
            all_quotes.append(q.quote)

    redis_client.setex(cache_key, CACHE_TTL, json.dumps(all_quotes))

    if not all_quotes:
        print(f"У знайдених авторах {author_query} не було цитат.")
    else:
        print(f"Цитати, знайдені по запиту '{author_query}':\n")
        for q in all_quotes:
            print(f'\t— {q}')


def search_by_tag(tag_query):
    
    query_clean = tag_query.strip().lower()
    cache_key = f"cache:tag:{query_clean}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"[Redis Cache HIT] Дані завантажені з кешу для тега '{tag_query}':")
        quotes_list = json.loads(cached_data)
        if not quotes_list:
            print(f"Цитати по тегу '{tag_query}' не знайдені.")
            return
        for q in quotes_list:
            print(f"- {q['author']}: {q['quote']} (Теги: {q['tags']})")
        return

    print(f"[MongoDB Query] Поиск в базі даних...")
    
    quotes = Quote.objects(tags__istartswith=query_clean)

    if not quotes:
        print(f"Цитати з тегом, схожим на '{tag_query}', не знайдені.")
        redis_client.setex(cache_key, 60, json.dumps([]))
        return

    formatted_quotes = []
    for q in quotes:
        formatted_quotes.append({
            "author": q.author.fullname,
            "quote": q.quote,
            "tags": q.tags
        })

    redis_client.setex(cache_key, CACHE_TTL, json.dumps(formatted_quotes))

    for q in formatted_quotes:
        print(f"- {q['author']}: {q['quote']} (Теги: {q['tags']})")


def search_by_tags(tags_string):
    
    tags_list = [tag.strip() for tag in tags_string.split(',')]
    quotes = Quote.objects(tags__in=tags_list)
    
    if not quotes:
        print(f"Цитати, котрі містять теги {tags_string}, не знайдені.")
        return

    for q in quotes:
        author_name = q.author.fullname
        print(f"- {author_name}: {q.quote} (Теги: {q.tags})")


def main():
    print("Скрипт пошуку цитат запущен. Доступні команди: name:, tag:, tags:, exit")
    
    while True:
        user_input = input("\nВведіть команду: ").strip()
        
        if user_input.lower() == 'exit':
            print("Завершення роботи скрипту. До побачення!")
            break
            
        if ':' not in user_input:
            print("Помилка: Неправильний формат. Використовуйте формат 'команда: значення'.")
            continue
            
        command, value = user_input.split(':', 1)
        command = command.strip().lower()
        value = value.strip()
        
        if not value:
            print("Помилка: Значення команди не може быть порожнім.")
            continue
            
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