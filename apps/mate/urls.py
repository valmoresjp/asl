from django.urls import include, path
from apps.mate import views


urlpatterns = [
         path('',                      views.inicio, name="inicio_mate"),
         path('agregar/',              views.agregar,name="agregar_mate"),
         path('editar/<int:idinsm>/',  views.editar,name= "editar_mate"),
         path('eliminar/<int:idinsm>/',views.eliminar,name="eliminar_mate"),
         ]
