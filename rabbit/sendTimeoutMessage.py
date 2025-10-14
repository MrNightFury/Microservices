import pika
import sys

connect = pika.BlockingConnection(pika.ConnectionParameters('51.250.26.59', 5672, credentials=pika.PlainCredentials('guest', 'guest123')))
channel = connect.channel()

channel.queue_declare(queue='IKBO-06-22_Vokhrin')
channel.basic_qos(prefetch_count=1)

message = "." * int(sys.argv[1])


channel.basic_publish(exchange='', routing_key='IKBO-06-22_Vokhrin', body=message)
channel.close()