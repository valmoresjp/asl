
from django.urls import include, path
from apps.conf import views

urlpatterns = [
    path('',                       views.inicio, name="inicio_conf"),
    path('agregar/',               views.agregar,  name="agregar_conf"),
    path('editar/<int:idconf>/',   views.editar, name="editar_conf"),
    path('eliminar/<int:idconf>/', views.eliminar, name='eliminar_conf'),
    # ~ path('detallar/<int:idprod>/',                    views.detallar,name='detallar_producto'),
    # ~ path('detallar/	<int:codp>/agregar/<int:codi>', views.agregar, name='agregar_insumo'),
    # ~ path('cuantificar/<int:codp>/',                views.cuantificar,name='cuantificar'),
    # ~ path('cuantificarv2/<int:codp>/',                views.cuantificarv2,name='cuantificarv2'),

    ]
