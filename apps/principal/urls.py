"""v01a URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path, include
from apps.principal import views


urlpatterns = [
	path('usuario/nuevo', views.usuario_nuevo, name="usuario_nuevo"),
	path('usuario/nousuario', views.nousuario, name="nousuario_principal"),
	path('privado/', views.privado, name="privado_principal"),
	path('cerrar', views.cerrar, name="cerrar_principal"),
	path('usuario/noactivo', views.noactivo, name="noactivo_principal"),
	path('ingreso', views.usuario_ingreso, name="usuario_ingreso"),
    path('',  views.inicio, name="inicio_principal"),
]
