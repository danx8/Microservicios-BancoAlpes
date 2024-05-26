from django.urls import path, include
#from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('clientes/', views.cliente_list, name='clienteList'),
    path(r'', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    
    #url(r'^clientes/', views.ClienteList),
    #url(r'^clientecreate/$', csrf_exempt(views.ClienteCreate), name='clienteCreate'),
    #url(r'^createclientes/$', csrf_exempt(views.ClientesCreate), name='createClientes'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)