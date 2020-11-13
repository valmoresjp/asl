
from django.urls import include, path
from apps.ventas import views


urlpatterns = [
         path('',                      views.inicio, name="inicio_ventas"),
         path('resumen/<int:ayo>/',               views.resumen, name="resumen_ventas"),
         path('agregar/<int:idprod>/<int:cantidad>',  views.agregar,name="agregar_ventas"),
         path('estado/<int:idventa>/<int:estado>',  views.estado,name="estado_ventas"),
         ]
