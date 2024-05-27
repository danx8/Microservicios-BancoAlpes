from datetime import date
import sys
from django.forms import model_to_dict
from .models import Cliente
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404

from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from .auth0backend import getRole
from .auth0backend import getEmail
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm, InformacionAdicionalForm
from .logic.cliente_logic import get_cliente, create_cliente
import requests
import json
import pika 


from .rabbit_const import *


connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host,credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

@login_required
def cliente_list(request):
    role = getRole(request)
    print("CLIENTE_LIST std",file=sys.stderr)
    print("CLIENTE_LIST none")
    print(role) 
    email = getEmail(request)
    print(email) 
    if role != "Administrador" and role != "Empleado" :
        form = ClienteForm()
        context = {
            'form': form,
        }
        return render(request, 'Cliente/clienteFailed.html', context)
     
      
    clientes = get_cliente()
    context = {
            'cliente_list': clientes
    }
    return render(request, 'Cliente/clientes.html', context)

@login_required
def cliente_account(request):
    role = getRole(request)
    email = getEmail(request)
    
    if role != "Administrador" and role != "Empleado" and role != "Normal" :
        form = ClienteForm()
        context = {
            'form': form,
        }
        return render(request, 'Cliente/clienteFailed.html', context)
    
    try:
        cliente = get_object_or_404(Cliente, correo=email)
        form = ClienteForm(instance=cliente)
        context = {
            'form': form,
            'cliente': cliente,
        }
        return render(request, 'Cliente/account.html', context)
    except Http404:
        return render(request, 'Cliente/clienteEmailFailed.html')
    
@login_required
def cliente_create(request):
    role = getRole(request)
    if role != "Administrador":
        form = ClienteForm()

        context = {
            'form': form,
        }
        return render(request, 'Cliente/clienteCreateFailed.html', context)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            create_cliente(form, channel)
            messages.add_message(request, messages.SUCCESS, 'Successfully created cliente')
            #return redirect(reverse('cliente_list'))

            return HttpResponseRedirect(reverse('clientes_create'))
        else:
            print(form.errors)
    else:
        form = ClienteForm()

    context = {
        'form': form,
    }
    return render(request, 'Cliente/clienteCreate.html', context)

@login_required
def cliente_edit(request, cliente_id):
    # Obtener el cliente que se desea editar
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    role = getRole(request)
    
    # Verificar si el usuario tiene permisos de Administrador
    if role != "Administrador":
        return render(request, 'Cliente/clienteEditFailed.html')
    
    if request.method == 'POST':
        # Rellenar el formulario con los datos del cliente existente
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            # Guardar los cambios si el formulario es válido
            #form.save()
            instance = form.save(commit=False)  
            
            instance_dict = model_to_dict(instance)
            json_data = json.dumps(instance_dict, cls=DateTimeEncoder)
            
            print('json---',json_data)
            
            
            channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
           
            channel.basic_publish(exchange=exchange, body=json_data, routing_key= routing_key, properties=pika.BasicProperties(delivery_mode=2, ))            
                        
                        
                        
                        
            messages.success(request, 'Cliente updated successfully')
            form = ClienteForm()
            context = {
                'form': form,
            }
            
            
            
            return render(request, 'Cliente/clienteEditSave.html', context)
    else:
        # Si no es una solicitud POST, mostrar el formulario con los datos del cliente
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
    }
    return render(request, 'Cliente/clienteEdit.html', context)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


@login_required
def cliente_borrar(request, cliente_id):  
    role = getRole(request)
    if role != "Administrador":
        form = ClienteForm()
        context = {
            'form': form,
        }
        return render(request,  'Cliente/clienteDeleteFailed.html', context)
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return HttpResponseRedirect(reverse('clientes_list'))
    
    context = {
        'cliente': cliente,
    }
    return render(request, 'Cliente/clienteBorrar.html', context)






def check_variable(data):
    r = requests.get(settings.PATH_VAR, headers={"Accept":"application/json"})
    variables = r.json()
    for variable in variables:
        if data["variable"] == variable["id"]:
            return True
    return False

def check_place(data):
    r = requests.get(settings.PATH_PLACES, headers={"Accept":"application/json"})
    places = r.json()
    for place in places:
        if data["place"] == place["name"]:
            return True
    return False



def clientes_list(request):
    queryset = Cliente.objects.all()
    context = list(queryset.values('id', 'variable', 'value', 'unit', 'place', 'dateTime'))
    return JsonResponse(context, safe=False)

def clientes_create(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        if check_variable(data_json) == True and check_place(data_json) == True :
            cliente = Cliente()
            cliente.variable = data_json['variable']
            cliente.value = data_json['value']
            cliente.unit = data_json['unit']
            cliente.place = data_json['place']
            cliente.save()
            return HttpResponse("successfully created cliente")
        else:
            return HttpResponse("unsuccessfully created cliente. Variable does not exist")
        
        

def ClientesCreate(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        cliente_list = []
        for cliente in data_json:
                    if check_variable(cliente) == True and check_place(data_json) == True:
                        db_cliente = Cliente()
                        db_cliente.variable = cliente['variable']
                        db_cliente.value = cliente['value']
                        db_cliente.unit = cliente['unit']
                        db_cliente.place = cliente['place']
                        cliente_list.append(db_cliente)
                    else:
                        return HttpResponse("unsuccessfully created cliente. Variable does not exist")
        
        Cliente.objects.bulk_create(cliente_list)
        return HttpResponse("successfully created clientes")
    
    
@login_required
def cliente_tarjeta(request):
    #role = getRole(request)
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            create_cliente(form, channel)
            messages.add_message(request, messages.SUCCESS, 'Successfully created cliente')
            #return redirect(reverse('cliente_list'))

            return HttpResponseRedirect(reverse('clientes_create'))
        else:
            print(form.errors)

        context = {'form': form}
        return render(request, 'Cliente/clienteCreateTarjeta2.html', context) 
    
    ### Entra aqui porque es GET
    email = getEmail(request)
    
    try:
        cliente = get_object_or_404(Cliente, correo=email)
        form = ClienteForm(instance=cliente)
        context = {
            'form': form,
            'cliente': cliente,
        }
        return render(request, 'Cliente/clienteEmailFailed.html', context)
    except Http404:
        
        form = ClienteForm(instance=None)
        context = {
            'form': form,
        }
        
        return render(request, 'Cliente/clienteCreateTarjeta2.html',  context)
