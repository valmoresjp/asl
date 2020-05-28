from django.urls import include, path
from apps.mate import views


urlpatterns = [
         path('',views.inicio, name="inicio_mate"),
         path('agregar/',views.agregar,name="agregar_mate"),
         ]
