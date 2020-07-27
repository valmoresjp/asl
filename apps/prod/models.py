from django.db import models
from datetime import datetime
from apps.mate.models import InsumosM
# ~ from apps.partida.models import PartidasM

# Create your models here.


class ProductosDetallesM(models.Model):
	idprd  = models.IntegerField() #id del producto
	idpart = models.IntegerField() #	id de la partida
	unid = models.CharField(max_length=10)	 # unidad de medida
	cant = models.FloatField() #cantidad

class ProductosM(models.Model):
	nomb      = models.CharField(max_length=40) #Nombre del producto
	codp      = models.CharField(max_length=20)  #Codigo del producto
	desc      = models.CharField(max_length=1000)# descripcion del producto
	unid      = models.CharField(max_length=10) # unidad de medida del producto
	insm   	  = models.FloatField(default=0.0) #insumos
	mate      = models.FloatField(default=0.0) #materiales
	pers      = models.FloatField(default=0.0) #personal
	serv      = models.FloatField(default=0.0) #servicios
	pinsm     = models.FloatField(default=30.0) #porcentaje de utilidad con respecto a los insumos
	pmate     = models.FloatField(default=30.0) # porcentaje de utilidad con respecto a los   materiales
	ppers     = models.FloatField(default=30.0) #porcentaje de utilidad con respecto al personal
	pserv     = models.FloatField(default=30.0) #porcentaje de utilidad con respecto a los  servicios
	utlds     = models.FloatField(default=0.0) #utilidades totales
	costo     = models.FloatField(default = 0.0) # costo totaldel producto
	fhcrea	  = models.DateTimeField(auto_now_add=True)
	fhactu 	  = models.DateTimeField(auto_now=True)
	# ~ fhentr    = models.DateTimeField(null=True, blank=True)
	def prinsm(self):
		return ( round((self.pinsm*self.insm)/100,2) )

	def prmate(self):
		return ( round((self.pinsm*self.mate)/100,2) )

	def prpers(self):
		return ( round((self.ppers*self.pers)/100,2) )

	def prserv(self):
		return ( round((self.pserv*self.serv)/100,2) )
<<<<<<< HEAD

class MaquiyHerraM(models.Model):
	idism = models.IntegerField() #id del insumo, vinculada con la tabal InsumosM
	idprd = models.IntegerField() #id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	unid = models.CharField(max_length=10)   #unidad de medida
	cant = models.FloatField(default = 1.0)              #cantidad

class CstsAdnlsM(models.Model):
	idcstanls = models.IntegerField()#id del costo adicional ubicado en la tabla CostosDescripcionM
	idprd    = models.IntegerField()#id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	cumedida = models.FloatField(default = 1.0)
	cant     = models.FloatField(default = 0.0)

	def total(self):
		return (round(self.cant*self.cumedida,2))

  # ~ Nuevas tablas para mejorar el funcionamiento del sistema
=======
	
# ~ class MaquiyHerraM(models.Model):
	# ~ idism = models.IntegerField() #id del insumo, vinculada con la tabal InsumosM
	# ~ idprd = models.IntegerField() #id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	# ~ unid = models.CharField(max_length=4)   #unidad de medida
	# ~ cant = models.FloatField(default = 1.0)              #cantidad 
	
# ~ class CstsAdnlsM(models.Model):
	# ~ idcstanls = models.IntegerField()#id del costo adicional ubicado en la tabla CostosDescripcionM
	# ~ idprd    = models.IntegerField()#id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	# ~ cumedida = models.FloatField(default = 1.0)
	# ~ cant     = models.FloatField(default = 0.0)
	
	# ~ def total(self):
		# ~ return (round(self.cant*self.cumedida,2))
	
  # ~ Nuevas tablas para mejorar el funcionamiento del sistema 
>>>>>>> 6be65c8e5726b6be39b21e937e8909216ecd90fd
class PartidasPRDM(models.Model):
	idprd    = models.IntegerField() #id del producto
	idpart   = models.IntegerField() #	id de la partida
	unid     = models.CharField(max_length=10)	 # unidad de medida
	cant     = models.FloatField() #cantidad

class MaterialesM(models.Model):
	idprd    = models.IntegerField()#id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	idmate   = models.IntegerField()#id del costo adicional ubicado en la tabla CostosDescripcionM
	cumedida = models.FloatField(default = 1.0)
	cant     = models.FloatField(default = 0.0)

class ServiciosM(models.Model):
	idprd    = models.IntegerField()#id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	idserv   = models.IntegerField()#id del costo adicional ubicado en la tabla CostosDescripcionM
	cumedida = models.FloatField(default = 1.0)
	cant     = models.FloatField(default = 0.0)

class PersonalM(models.Model):
	idprd    = models.IntegerField()#id del producto al que esta asociado, vinculado con la tabla ProductosDetallesM
	idpers    = models.IntegerField()#id del costo adicional ubicado en la tabla CostosDescripcionM
	cumedida = models.FloatField(default = 1.0)
	cant     = models.FloatField(default = 0.0)

