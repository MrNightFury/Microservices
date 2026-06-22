import pika

connect = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost', 5672, credentials=pika.PlainCredentials('guest', 'guest123')))
channel = connect.channel()

channel.queue_declare(queue='awesome_queue')

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

channel.basic_consume(queue='awesome_queue', on_message_callback=callback, auto_ack=True)

channel.start_consuming()