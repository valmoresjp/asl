from django.db import models
from datetime import datetime

# Create your models here.

class VentasM(models.Model):
	idclie = models.IntegerField()
	idprod = models.IntegerField()
	costo  = models.FloatField(default=0.0)
	cant   = models.FloatField(default=0.0)
	insm   = models.FloatField(default=0.0) #insumos
	mate   = models.FloatField(default=0.0) #materiales
	pers   = models.FloatField(default=0.0) #personal
	serv   = models.FloatField(default=0.0) #servicios
	utlds  = models.FloatField(default=0.0) #utilidades
	obsrv  = models.CharField(max_length=500,default="") # Observaciones que se desean realizar
	direc  = models.CharField(max_length=100,default="Retiro en tienda") # direccion de entrega
	centr  = models.FloatField(default=0.0)# costo de entrega
	fhacd  = models.DateTimeField(auto_now_add=True, blank=True) # Fecha del momento que se suscribio el acuerdo
	fhentr = models.DateTimeField(null=True, blank=True)# Fecha de entrega del producto
	estado = models.CharField(max_length=6,default='EN_PRO')
	
	def dias(self):
		entrega  = datetime(self.fhentr.year,self.fhentr.month,self.fhentr.day,self.fhentr.hour,self.fhentr.minute)
		dias = entrega - datetime.now()
		return (dias.days)
		
	
class ResumenM(models.Model):
	
	## es importante tener encuenta que las estadidiscas se registran con la fecha en 
	## el momento que se realizo el acuerdo y no cuando se entrega el producto
	ayo  = models.IntegerField(default=0)
	mes  = models.IntegerField(default=0)
	ncli = models.IntegerField(default=0) # numero de clientes
	nped = models.IntegerField(default=0) # numero de pedidos
	
	tota = models.IntegerField(default=0) # total vendido en semana 1
	util = models.FloatField(default=0) # utilidades
	insm = models.FloatField(default=0) # insumos
	mate = models.FloatField(default=0) # materiales
	pers = models.FloatField(default=0) # personal
	serv = models.FloatField(default=0) # servicio
		
