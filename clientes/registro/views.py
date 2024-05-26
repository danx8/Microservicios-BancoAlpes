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
import requests
import json
import pika 


from .rabbit_const import *


connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host,credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

def index(request):
    return render(request, 'index.html')

def terminosycondiciones(request):
    return render(request, 'registro/terminos_y_condiciones.html')

def healthcheck(request):
    return HttpResponse("ok")

def intento(request):
    return render(request, 'registro/intento.html')