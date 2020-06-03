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
from django.contrib import admin
admin.autodiscover()

from apps.mate import views
from apps.partida import views
from apps.prod import views
from apps.principal import views


urlpatterns = [
<<<<<<< HEAD
#    path('admin/', admin.site.urls),
    path('',  include("apps.principal.urls")),
=======
	path('admin/', admin.site.urls),
    path('inicio/',  include("apps.principal.urls")),
>>>>>>> dc6ffa78b9ae859101736760ebd50bf7fa11c110
    path('insumos/', include("apps.mate.urls")),
    path('partidas/', include("apps.partida.urls")),
    path('productos/', include("apps.prod.urls")),
    path('configuracion/', include("apps.conf.urls")),
]
