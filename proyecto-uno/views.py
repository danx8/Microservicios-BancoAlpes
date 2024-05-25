from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

def terminosycondiciones(request):
    return render(request, 'terminosYCondiciones.html')

def healthcheck(request):
    return HttpResponse("ok")

def intento(request):
    return render(request, 'intento.html')

