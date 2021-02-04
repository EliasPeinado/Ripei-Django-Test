from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.urls
from .views import home, commercialize, contacto, transferir, registro, buySell, CritoViewset,info
from rest_framework import routers

router = routers.DefaultRouter()
router.register('crito', CritoViewset)

urlpatterns = [
    path('', home, name = 'home'),
    path('commercialize/', commercialize, name = 'commercialize'),
    path('contacto/', contacto, name = 'contacto'),
    path('transferir/', transferir, name = 'transferir'),
    path('registro/', registro, name = 'registro'),
    path('buySell/', buySell, name = 'buySell'),
    path('info/', info, name = 'info'),


    path('api/', include(router.urls)),

]