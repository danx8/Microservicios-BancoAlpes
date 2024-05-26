from django.urls import path, include
#from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



from . import views

urlpatterns = [
    path('', views.index),
    path('registro/terminos-y-condiciones', views.terminosycondiciones),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)