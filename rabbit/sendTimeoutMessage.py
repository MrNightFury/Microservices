import pika
import sys

connect = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, credentials=pika.PlainCredentials('guest', 'guest')))
channel = connect.channel()

channel.queue_declare(queue='IKBO-26-22_Vokhrin', durable=True)
channel.basic_qos(prefetch_count=1)

message = "." * int(sys.argv[1])


channel.basic_publish(exchange='', routing_key='IKBO-26-22_Vokhrin', body=message)
channel.close()