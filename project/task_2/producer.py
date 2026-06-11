import pika
import json
from faker import Faker
from models import Contact

def main():
    fake = Faker() 
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    queue_name = 'email_queue'
    channel.queue_declare(queue=queue_name, durable=True)
    
    print(f"Генерація контактів та надсилання в чергу '{queue_name}'...")

    for _ in range(10):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            subject=fake.sentence(nb_words=4)
        )
        contact.save()  

        message = {
            'contact_id': str(contact.id)
        }
        
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  
            )
        )
        print(f" [+] Згенеровано контакт: {contact.fullname} | ID додано в чергу: {contact.id}")

    connection.close()
    print("Усі контакти успішно оброблені продюсером.")

if __name__ == '__main__':
    main()
