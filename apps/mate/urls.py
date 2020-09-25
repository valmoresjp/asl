from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from apps.mate import views


urlpatterns = [
         path('',                      views.inicio, name="inicio_mate"),
         path('agregar/<int:idfactu>/', views.agregar,name="agregar_mate"),
         path('editar/<int:idinsm>/',  views.editar,name= "editar_mate"),
         path('eliminar/<int:idinsm>/',views.eliminar,name="eliminar_mate"),
         path('factura/agregar/',views.agregar_factura,name="agregar_factura_mate"),
         path('factura/listar/',views.listar_factura,name="listar_factura_mate"),
         path('factura/contenido/<int:idfactu>/',views.contenido_factura,name="contenido_factura_mate"),
         path('factura/item/<int:idfactu>/<int:idinsm>/',views.item_factura,name="item_factura_mate"),
         path('factura/compras/<int:idinsm>/',views.compras_mate,name="compras_mate"),
         path('factura/descarga/<int:idfactu>/',views.descarga_factura,name="descarga_factura"),
         # ~ path('factura/listar/<int:idfactu>Facturas/<str:ru	ta>/',views.descarga_factura,name="descarga_factura"),
         ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
