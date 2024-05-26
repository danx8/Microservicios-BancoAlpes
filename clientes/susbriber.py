import pika

rabbit_host = '10.128.0.6'
rabbit_user = 'monitoring_user'
rabbit_password = 'isis2503'
exchange = 'clientes_exchange'
routing_key='clientes'

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # Aquí puedes procesar el mensaje como necesites
    # Por ejemplo, convertirlo de JSON a un diccionario de Python si es necesario
    # import json
    # message = json.loads(body)
    # print("Processed message:", message)

def main():
    # Conéctate a RabbitMQ
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host,credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
   

    # Declara la cola
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Enlaza la cola al intercambio
    channel.queue_bind(exchange= exchange, queue=queue_name, routing_key=routing_key)

    # Configura el consumidor
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
