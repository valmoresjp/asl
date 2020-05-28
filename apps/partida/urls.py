"""v3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from apps.partida import views

urlpatterns = [
    path('',                                       views.inicio, name="inicio_partida"),
    path('nuevo/',                                 views.nuevo,  name="nuevo_partida"),
    path('editar/<int:idpart>/',                      views.editar, name="editar_partida"),
    path('eliminar/<int:idpart>/',                    views.eliminar, name='eliminar_partida'),
    path('detallar/<int:idpart>/',                    views.detallar,name='detallar_partida'),
    # ~ path('detallar/	<int:codp>/agregar/<int:codi>', views.agregar, name='agregar_insumo'),
    # ~ path('cuantificar/<int:codp>/',                views.cuantificar,name='cuantificar'),
    # ~ path('cuantificarv2/<int:codp>/',                views.cuantificarv2,name='cuantificarv2'),

    ]

  

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
