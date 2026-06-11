import pika
import json
import time
from models import Contact

def send_email_stub(fullname, email, subject):
    """Функція-заглушка для імітації надсилання листа."""
    print(f" [->] Надсилання email для: {fullname} ({email})...")
    print(f"      Тема листа: '{subject}'")
    time.sleep(1.5) 
    print(" [✓] Лист успішно надіслано!")

def callback(ch, method, properties, body):
    """Колбек-функція, яка викликається при надходженні нового повідомлення."""
    try:
        data = json.loads(body.decode('utf-8'))
        contact_id = data.get('contact_id')
        
        contact = Contact.objects(id=contact_id).first()
        
        if contact:
            if not contact.is_sent:
                send_email_stub(contact.fullname, contact.email, contact.subject)
        
                contact.update(set__is_sent=True)
                print(f" [База Даних] Статус контакту {contact_id} змінено на is_sent=True\n")
            else:
                print(f" [!] Контакт {contact_id} вже оброблений раніше.")
        else:
            print(f" [Помилка] Контакт з ID {contact_id} не знайдений у MongoDB.")
            
    except Exception as e:
        print(f" [Помилка обробки]: {e}")
        
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    queue_name = 'email_queue'
    channel.queue_declare(queue=queue_name, durable=True)
    
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    
    print(' [*] Очікування повідомлень. Для виходу натисніть CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nСкрипт зупинено користувачем.')
