from django.db import models
from django.db.models import Sum
from django.db.models.functions import Round
from apps.ventas.models import VentasM

# Create your models here.


class ClientesM(models.Model):
	idrefe   = models.IntegerField(default=1)
	nombre   = models.CharField(max_length=40)
	telefono = models.CharField(max_length=15)
	correo	 = models.EmailField(max_length=128, unique=True, null=True, blank=True)
	fhaniver = models.DateTimeField(null=True, blank=True)# Fecha de cumpleaños
	fhreg    = models.DateTimeField(auto_now_add=True, blank=True) # Fecha del momento que se suscribio el acuerdo
	
	def total_adq(self):
		adq = VentasM.objects.filter(idclie=self.id).filter(estado__gte=1, estado__lte=3).aggregate(total=Sum('costo'))
		if adq['total']==None:
			adq['total'] = 0.0
		return ( adq['total'] )
	
	def total_pedidos(self):
		pedds = VentasM.objects.filter(idclie=self.id).aggregate(pdds=Sum('cant'))
		if pedds['pdds']==None:
			pedds['pdds'] = 0.0
		return ( pedds['pdds'] )

class ReferidosM(models.Model):
	nombre   = models.CharField(max_length=40, default="ASL")
	telefono = models.CharField(max_length=15)
	fhreg  = models.DateTimeField(auto_now_add=True, blank=True) # Fecha del momento que se suscribio el acuerdo
