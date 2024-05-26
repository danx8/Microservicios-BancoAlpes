from ..models import Cliente
from datetime import date
from django.forms import model_to_dict
import json
import pika
from ..rabbit_const import *

def get_cliente():
    queryset = Cliente.objects.all()
    return (queryset)

def create_cliente(form, channel):
    
    instance = form.save(commit=False)  
            
    instance_dict = model_to_dict(instance)
    json_data = json.dumps(instance_dict, cls=DateTimeEncoder)
            
    print('json---',json_data)
                
    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)       
    channel.basic_publish(exchange=exchange, body=json_data, routing_key= routing_key, properties=pika.BasicProperties(delivery_mode=2, ))            
            
    
    
    cliente = form.save()
    cliente.save()
    return ()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)