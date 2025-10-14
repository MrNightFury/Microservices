import pika

connect = pika.BlockingConnection(pika.ConnectionParameters('51.250.26.59', 5672, credentials=pika.PlainCredentials('guest', 'guest123')))
channel = connect.channel()
channel.queue_declare(queue='IKBO-32-22_Vokhrin')

channel.basic_consume(queue='IKBO-32-22_Vokhrin',
                      on_message_callback=lambda ch, method, properties, body: print(f" [x] Received {body}"),
                      auto_ack=True)

channel.start_consuming()