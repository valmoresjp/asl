from django.db import models
from django.db.models import  Count, Sum
from datetime import datetime,date

# Create your models here.
class InsumosM(models.Model):

	# CODIGO: Codigo internor del producto 
	# FINGSO: Fecha de Ingreso del producto. Este campo debe ser cargado automaticamente
	# DESCRP: Descripcion del producto
	# UMEDIDA: Unidad de medida del producto (metros lineales, mtsl. Unidad, und. Litros, lts. etc)
	# DISTB(n): Nombre del distribuidor del producto. Hay capacidad para 5 distrbuidores.
	# COSTO(N): Costo del producto por distribuidor.
	# cmedi(n): Costo por unidad de medida
	# FACTU(n): Fecha de actualización del producto para el producto n(donde n va de 1 a 5).

	codigo   = models.CharField(max_length=26) 
	# El codigo se debe crear de la siguiente forma 3 dgitos para el tipo de insumo
	# es decir INGREDIENTE, PERSONAL, MATERIALES, etc. Luego 3 digitos para el 
	# INGREDIENTE:
	#   tipo        = 100
	#   correlativo = 0000 (creado automaticamente)
	#   futuro      = 0000
	
	descrip  = models.CharField(max_length=60)
	umedida  = models.CharField(max_length=5) # valor real del costo por unidad de medida segun la compra realizada
	#Costo Por Unidad de Medida Calculado(cumedcal): promedio del valor anterior y el actual, este valor trata de compensar la diferencia que pueda haber con respecto
	#al ultimo valor del costo por unidad de medida. Es decir, si hay producto en el inventario adquiido a un costo distinto 
	# (de mayor valor que la compra actual) se calculara el promedio delcalulo actual con respecto al anterior y ese sera el valor calculado.
	cumedcal = models.FloatField(default = 1.00) 
	cantd   = models.FloatField(default = 1.00)
	inven   = models.FloatField(default = 0.0)
	tipo    = models.CharField(max_length=4)
	costop	= models.FloatField(default=0.00)
	costot	= models.FloatField(default=0.00)
	
	def cumedida(self):
		cumd = (self.costop + self.costot)/self.cantd
		return (round(cumd,2))
		
	def ctotal(self):
		return ( round(self.costop + self.costot,2) )
		

class ComprasM(models.Model):
	idinsm  = models.IntegerField()
	costop  = models.FloatField(default = 0.0) #costo del producto
	costot  = models.FloatField(default = 0.0) #costo del transporte segun la cantida de productos de la factura, es decir, se divide el costo del transporte entre el numero de productos de la factura
	cantd   = models.FloatField(default = 0.0)
	umedida = models.CharField(max_length=5)
	idfactu = models.IntegerField()      ## id de la factura
	fhcomp  = models.DateField()# Fecha de compra
	# ~ archivo = models.FileField(upload_to='facturas')
	
	def cumedida(self):
		cumd = (self.costop + self.costot)/self.cantd
		
		# ~ return (round(cumd,2))
		return (cumd)
	
	def ctotal(self):
		ctotal = self.costop + self.costot
		return (round(ctotal,2))
		
	
class FacturasM(models.Model):
	codigo  = models.CharField(max_length=24,default="")
	# El codigo esta formado por 3 caracteres mas 4 digitos(correlativo, agregado automaticamente)
	# ING = ingrediente
	# MAT = material
	# SER = servicio
	# MYH = Maquinas y Herramientas
	# PER = Personal
	emisor  = models.CharField(max_length=24,default="") 
	numero  = models.IntegerField(default=0)
	total   = models.FloatField(default=0.0)
	fhfactu = models.DateField()# Fecha de compra
	transp  = models.FloatField(default=0.0)
	archivo = models.FileField(upload_to='facturas/')
	observ  = models.CharField(max_length=500,default="") 
	

	def compra_total(self):
		compras = ComprasM.objects.filter(idfactu=self.id).aggregate(cp=Sum('costop'),ct=Sum('costot'))
		if  not compras['cp']:
			 compras['cp'] = 0.0
		if  not compras['ct']:
			 compras['ct'] = 0.0
		# ~ return( compras['cp'] + compras['cp'])
		return( self.total + self.transp)
