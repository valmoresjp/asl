from django.conf import settings
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
	# ~ imagen1   = models.ImageField(null=True, blank=True)
	# ~ imagen2   = models.ImageField(null=True, blank=True)
	# ~ imagen3   = models.ImageField(upload_to='facturas/',null=True, blank=True)
	# ~ fhentr    = models.DateTimeField(null=True, blank=True)
	def prinsm(self):
		return ( round((self.pinsm*self.insm)/100,2) )
		
	def prmate(self):
		return ( round((self.pinsm*self.mate)/100,2) )
		
	def prpers(self):
		return ( round((self.ppers*self.pers)/100,2) )
		
	def prserv(self):
		return ( round((self.pserv*self.serv)/100,2) )
		
class ImagenesM(models.Model):
	idprod =  models.IntegerField() # id del producto
	img1   =  models.ImageField(upload_to='imagenes/',null=True, blank=True)
	img2   =  models.ImageField(upload_to='imagenes/',null=True, blank=True)
	img3   =  models.ImageField(upload_to='imagenes/',null=True, blank=True)
	img4   =  models.ImageField(upload_to='imagenes/',null=True, blank=True)
	
	def imagen1(self):
		img = settings.MEDIA_URL + 'imagenes/SiS.png'
		if self.img1:
			img = self.img1.url
		return (img)
		
	def imagen2(self):
		img = settings.MEDIA_URL + 'imagenes/SiS.png'
		if self.img2:
			img = self.img2.url
		return (img)
		
	def imagen3(self):
		img = settings.MEDIA_URL + 'imagenes/SiS.png'
		if self.img3:
			img = self.img3.url
		return (img)
		
	def imagen4(self):
		img = settings.MEDIA_URL + 'imagenes/SiS.png'
		if self.img4:
			img = self.img4.url
		return (img)
		
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

