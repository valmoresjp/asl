
from django.urls import include, path
from apps.conf import views

urlpatterns = [
    path('',                       views.inicio, name="inicio_conf"),
    path('agregar/',               views.agregar,  name="agregar_conf"),
    path('editar/<int:idconf>/',   views.editar, name="editar_conf"),
    path('eliminar/<int:idconf>/', views.eliminar, name='eliminar_conf'),
    ]
