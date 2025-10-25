from time import sleep
import pika

connect = pika.BlockingConnection(pika.ConnectionParameters('51.250.26.59', 5672, credentials=pika.PlainCredentials('guest', 'guest123')))
channel = connect.channel()

channel.queue_declare(queue='IKBO-26-22_Vokhrin')
channel.basic_qos(prefetch_count=1)

def delayed_callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")

channel.basic_consume(queue='IKBO-26-22_Vokhrin',
                      on_message_callback=delayed_callback)

channel.start_consuming()