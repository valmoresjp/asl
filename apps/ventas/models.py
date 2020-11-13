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
	estado = models.IntegerField(default=0)
	
	def dias(self):
		entrega  = datetime(self.fhentr.year,self.fhentr.month,self.fhentr.day,self.fhentr.hour,self.fhentr.minute)
		dias = entrega - datetime.now()
		return (dias.days)
	
	def estado_producto(self):
		e = 'POR APROBACION'
		if self.estado == 1:
			e = 'EN PROCESO'
		if self.estado == 2:
			e = 'EN RUTA'
		if self.estado == 3:
			e = 'ENTREGADO'
		if self.estado == 99:
			e = 'CANCELADO'
		return (e)
	
class ResumenM(models.Model):
	
	## es importante tener encuenta que las estadidiscas se registran con la fecha en 
	## el momento que se realizo el acuerdo y no cuando se entrega el producto
	ayo  = models.IntegerField(default=0)
	mes  = models.IntegerField(default=0)
	ncli_t = models.IntegerField(default=0) # clientes totales (mes anterior + mes actual )
	ncli_n = models.IntegerField(default=0) # numero de clientes nuevos 
	ncli_a = models.IntegerField(default=0) # numero de clientes que compraron en el mes
	
	npeds  = models.IntegerField(default=0) # numero de pedidos solicitados( presupuestos)
	npedv  = models.IntegerField(default=0) # numero de pedidos vendidos (presupuestos)
	npedc  = models.IntegerField(default=0) # numero de pedidos cancelados (presupuestos)
	nprdv  = models.IntegerField(default=0) # numero de productos vendidos (dentro de un presupuesto podrian haber varios productos)
	
	tota = models.IntegerField(default=0) # total vendido 
	util = models.FloatField(default=0) # utilidades
	insm = models.FloatField(default=0) # insumos
	mate = models.FloatField(default=0) # materiales
	pers = models.FloatField(default=0) # personal
	serv = models.FloatField(default=0) # servicio
	
	# ~ ving = models.FloatField(default=0) # gasto en ingredientes(insumos comestibles)
	# ~ vmat = models.FloatField(default=0) # gasto en materiales(insumos no comestibles)
	# ~ vmyh = models.FloatField(default=0) # gasto en maquinas y herramientas(batidoras, hornos, neveras, moldes, cortadores, etc)
	
	# ~ ging = models.FloatField(default=0) # gasto en ingredientes(insumos comestibles)
	# ~ gmat = models.FloatField(default=0) # gasto en materiales(insumos no comestibles)
	# ~ gmyh = models.FloatField(default=0) # gasto en maquinas y herramientas(batidoras, hornos, neveras, moldes, cortadores, etc)

	def npedt (self):
		return ( self.npedv + self.npedc)

		
