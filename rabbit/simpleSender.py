import pika

connect = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost', 5672, credentials=pika.PlainCredentials('guest', 'guest')))
channel = connect.channel()

queue_name = 'awesome_queue'
channel.queue_declare(queue=queue_name)

channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body='Hello World!',
                      properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
print('SENT: My first message') 

channel.close()

exchange = channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.basic_publish(
    exchange='logs',
    routing_key='',
    body='Hello World!'
)

queue = channel.queue_declare(queue='', exclusive=True)

queue_name = queue.method.queue
exchange_name = 'logs'
channel.queue_bind(exchange=exchange_name, queue=queue_name)


exchange_dir = channel.exchange_declare(exchange='logs', exchange_type='direct')
channel.queue_bind(exchange='logs', queue=queue_name, routing_key='info')

channel.basic_publish(
    exchange='logs',
    routing_key='info',
    body='Hello World!'
)

exchange_top = channel.exchange_declare(exchange='currency', exchange_type='topic')
channel.queue_bind(exchange='currency', queue=queue_name, routing_key='*.usa.*')

channel.basic_publish(exchange='currency', routing_key='usd.usa.eur', body='Hello World!')