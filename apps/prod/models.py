from django.db import models
from datetime import datetime
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM

# Create your models here.


class ProductosDetallesM(models.Model):
	idprd  = models.IntegerField() #id del producto
	idpart = models.IntegerField() #id de la partida
	unid = models.CharField(max_length=10)	 # unidad de medida
	cant = models.FloatField() #cantidad
	# ~ item   = models.CharField(max_length=6)
	# ~ costo  = models.FloatField()  #costo en pesos chilenos 

class ProductosM(models.Model):
	nomb  = models.CharField(max_length=40) #Nombre del producto
	codp = models.CharField(max_length=20)  #Codigo del producto
	desc = models.CharField(max_length=1000)# descripcion del producto
	unid = models.CharField(max_length=10) # unidad de medida del producto
	costo = models.FloatField(default = 0.0) # costo totaldel producto
	
class MaquiyHerraM(models.Model):
	idism = models.IntegerField() #id del insumo, vinculada con la tabal InsumosM
	idprd = models.IntegerField() #id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	unid = models.CharField(max_length=4)   #unidad de medida
	cant = models.FloatField(default = 1.0)              #cantidad 
	
class CstsAdnlsM(models.Model):
	idcstanls = models.IntegerField()#id del costo adicional ubicado en la tabla CostosDescripcionM
	idprd = models.IntegerField()#id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	cumedida = models.FloatField(default = 1.0)
	cant = models.FloatField(default = 0.0)
	
	def total(self):
		return (round(self.cant*self.cumedida,2))
	
	
