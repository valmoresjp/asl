from django.db import models

# Create your models here.
class InsumosM(models.Model):


	TIPO_ELEMENTO = (
	 	 ('MAT','MATERIAL'),
	 	 ('PER','PERSONAL'),
	 	 ('MYH','MAQyHERR'),
	 	 ('SER','SERVICIO'),
	 	 ('ING','INGREDIENTE'),
	 	 )

	# CODIGO: Codigo internor del producto 
	# FINGSO: Fecha de Ingreso del producto. Este campo debe ser cargado automaticamente
	# DESCRP: Descripcion del producto
	# UMEDIDA: Unidad de medida del producto (metros lineales, mtsl. Unidad, und. Litros, lts. etc)
	# DISTB(n): Nombre del distribuidor del producto. Hay capacidad para 5 distrbuidores.
	# COSTO(N): Costo del producto por distribuidor.
	# cmedi(n): Costo por unidad de medida
	# FACTU(n): Fecha de actualización del producto para el producto n(donde n va de 1 a 5).

	codigo  = models.CharField(max_length=26)
	# ~ fingso  = models.DateTimeField(null=True, blank=True)
	descrip = models.CharField(max_length=60)
	umedida = models.CharField(max_length=5)
	cantd   = models.FloatField(default = 1.00)
	inven   = models.FloatField(default = 0.0)
	tipo    = models.CharField(max_length=14, choices=TIPO_ELEMENTO, default='ING')
	
	distb1  = models.CharField(max_length=30) 
	costo1	= models.FloatField(default=0.00)
	# ~ cmedi1  = models.FloatField(default=1.00)
	factu1	= models.DateTimeField(null=True, blank=True)
	
	distb2  = models.CharField(max_length=30, null=True, blank=True)
	costo2  = models.FloatField(default=0.00, null=True, blank=True)
	# ~ cmedi2  = models.FloatField(default=1.00, null=True, blank=True)
	factu2	= models.DateTimeField( null=True, blank=True)

	distb3  = models.CharField(max_length=30, null=True, blank=True)
	costo3  = models.FloatField(default=0.00, null=True, blank=True)
	# ~ cmedi3  = models.FloatField(default=1.00, null=True, blank=True)
	factu3	= models.DateTimeField( null=True, blank=True)

	distb4  = models.CharField(max_length=30, null=True, blank=True)
	costo4  = models.FloatField(default=0.00, null=True, blank=True)
	# ~ cmedi4  = models.FloatField(default=1.00, null=True, blank=True)
	factu4	= models.DateTimeField( null=True, blank=True)

	distb5  = models.CharField(max_length=30, null=True, blank=True)
	costo5  = models.FloatField(default=0.00, null=True, blank=True)
	# ~ cmedi5  = models.FloatField(default=1.00, null=True, blank=True)
	factu5	= models.DateTimeField( null=True, blank=True)
	
	# ~ ctprom  = models.FloatField(default=0.00, null=True, blank=True)
	# ~ ctmax   = models.FloatField(default=0.00, null=True, blank=True)
	# ~ ctmin   = models.FloatField(default=0.00, null=True, blank=True)
	def cmedi1(self):
		return ( round(self.costo1 / self.cantd,2) )
		
	def cmedi2(self):
		return ( round(self.costo2 / self.cantd,2) )
		
	def cmedi3(self):
		return ( round(self.costo3 / self.cantd,2) )
		
	def cmedi4(self):
		return ( round(self.costo4 / self.cantd,2) )
		
	def cmedi5(self):
		return ( round(self.costo5 / self.cantd,2) )
		
	def max(self):
		v = [self.costo1, self.costo2, self.costo3, self.costo4, self.costo5]
		valores = list(filter(lambda x:x>0, v))
		return( max(valores) )
	
	def min(self):
		v = [self.costo1, self.costo2, self.costo3, self.costo4, self.costo5]
		valores = list(filter(lambda x:x>0, v))
		return( min(valores) )
	
	def prom(self):
		v = [self.costo1, self.costo2, self.costo3, self.costo4, self.costo5]
		valores = list(filter(lambda x:x>0, v))
		return( round(sum(valores)/len(valores)) )
	
	def cumedida(self):
		#retorna el costo por unidad de medida maximo
		v = [self.costo1/self.cantd, self.costo2/self.cantd, self.costo3/self.cantd, self.costo4/self.cantd, self.costo5/self.cantd]
		return(round(max(v),2))
