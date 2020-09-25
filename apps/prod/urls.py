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
from apps.prod import views
# ~ from django.conf import settings
# ~ from django.conf.urls.static import static

urlpatterns = [
    path('',                          views.inicio,  name="inicio_producto"),
    path('nuevo/',                    views.nuevo,   name="nuevo_producto"),
    path('editar/<int:idprod>/',      views.editar,  name="editar_producto"),
    path('eliminar/<int:idprod>/',    views.eliminar,name='eliminar_producto'),
    path('detallar/<int:idprod>/',    views.detallar,name='detallar_producto'),
    path('detallar/presupuesto/<int:idprod>/',    views.presupuesto,name='presupuesto_producto'),
    path('detallar/imagenes/<int:idprod>/',       views.imagenes,   name="imagenes_producto"),
    # ~ path('*.jpg/',       views.imagenes,   name="imagenes_producto"),
    ]

	# ~ if settings.DEBUG:
# ~ urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
