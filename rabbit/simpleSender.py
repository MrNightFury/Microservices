import pika

connect = pika.BlockingConnection(pika.ConnectionParameters(
    '51.250.26.59', 5672, credentials=pika.PlainCredentials('guest', 'guest123')))
channel = connect.channel()

channel.queue_declare(queue='IKBO-26-22_Vokhrin')
channel.basic_publish(exchange='',
                      routing_key='IKBO-26-22_Vokhrin',
                      body='Hello World!')

channel.close()