from .models import Cliente
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import requests
import json

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



def ClienteList(request):
    queryset = Cliente.objects.all()
    context = list(queryset.values('id', 'variable', 'value', 'unit', 'place', 'dateTime'))
    return JsonResponse(context, safe=False)

def ClienteCreate(request):
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