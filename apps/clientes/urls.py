
from django.urls import include, path
from apps.clientes import views


urlpatterns = [
         path('',                      views.inicio, name="inicio_clientes"),
         path('agregar/',              views.agregar,name="agregar_clientes"),
         path('editar/<int:idclie>/',  views.editar,name= "editar_clientes"),
         path('detallar/<int:idclie>/',  views.detallar,name= "detallar_clientes"),
         # ~ path('eliminar/<int:idinsm>/',views.eliminar,name="eliminar_clientes"),
         ]
