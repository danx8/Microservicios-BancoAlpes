from django.urls import path, include
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('clientes/', views.cliente_list, name='clienteList'),
    url(r'^clientes/', views.ClienteList),
    url(r'^clientecreate/$', csrf_exempt(views.ClienteCreate), name='clienteCreate'),
    url(r'^createclientes/$', csrf_exempt(views.ClientesCreate), name='createClientes'),
]