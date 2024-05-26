import pika
import json

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clientes.settings')
import django
django.setup()
from clientes.models import Cliente
from clientes.rabbit_const import *


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    json_to_model(body)
    
    
    
    # Aquí puedes procesar el mensaje como necesites
    # Por ejemplo, convertirlo de JSON a un diccionario de Python si es necesario
    # import json
    # message = json.loads(body)
    # print("Processed message:", message)



def json_to_model(json_string):
    # Deserialize JSON string into Python dictionary
    data = json.loads(json_string)

    # Create a new Clientes model instance using the dictionary
    cliente = Cliente(**data)
    
    # Save the model instance to the database if needed
    cliente.save()

    return cliente



def main():
    # Conéctate a RabbitMQ
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host,credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
   

    # Declara la cola
    channel.queue_declare(queue=queue_name, durable=True)

    

    # Enlaza la cola al intercambio
    channel.queue_bind(exchange= exchange, queue=queue_name, routing_key=routing_key)

    # Configura el consumidor
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    
    
if __name__ == '__main__':
    main()
