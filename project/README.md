У цих завданнях використовувалися наступні бібліотеки:
    - mongoengine
    - pika
    - dotenv
    - sys
    - os
    - json
    - pathlib
    - bson
    - faker

models.py - створення моделей

upload_data.py - наповнення моделей данними 

queries.py - скрипт, для пошуку цитат за тегом, ім'ям автора або набором тегів

authors.json та qoutes.json - ім'я авторів та їх дані; цитати авторів та їх теги

consumer.py - скрипт отримувача

producer.py - скрипт відправника

models_rabbit.py - моделі для розсилки