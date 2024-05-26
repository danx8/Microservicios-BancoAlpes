from django.urls import path, include
#from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', include('registro.urls')),
    path('admin/', admin.site.urls),
    path('clientes/', views.cliente_list, name='clientes_list'),
    path('clientes/account/', views.cliente_account, name='account'),
    path('clientes/failed/', views.cliente_list, name='clientes_failed'),
    path('clientes/create/', csrf_exempt(views.cliente_create), name='clientes_create'),
    path('clientes/create/failed/', csrf_exempt(views.cliente_create), name='clientes_create_failed'),
    path('clientes/edit/<int:cliente_id>/', csrf_exempt(views.cliente_edit), name='clienteEdit'),
    path('clientes/delete/<int:cliente_id>/', views.cliente_borrar, name='clienteBorrar'),
    path('clientes/edit-save/', csrf_exempt(views.cliente_edit), name='clienteEditSave'),


    #path('clientecreate-jmeter/', csrf_exempt(views.cliente_create_jmeter), name='cliente_create_jmeter'),
    
    
    path('accounts/', include('django.contrib.auth.urls')),  # Default Django auth URLs
    
    
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),

    #path('login/auth0', include('social_django.urls')),  # Auth0 URL
    #url(r'^clientes/', views.clientes_list),
    #url(r'^clientecreate/$', csrf_exempt(views.ClienteCreate), name='clienteCreate'),
    #url(r'^createclientes/$', csrf_exempt(views.ClientesCreate), name='createClientes'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)