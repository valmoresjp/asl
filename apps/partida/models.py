from django.db import models
from datetime import datetime
from apps.mate.models import InsumosM

# Create your models here.
UNIDAD_DE_MEDIDA=(
    ('HRS', 'Horas'),
    ('HH', 'Horas Hombre'),
    ('UND', 'Unidad'),
    ('GL', 'Global'),
    ('HM', 'Horas Maquina'),
    ('MTS', 'Metros'),
    ('ML','Metros Lineales'),
)

class Cliente(models.Model):

	fecha       = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), blank=None, null=None)
	cliente     = models.CharField(max_length=20)
	proyecto    = models.CharField(max_length=60)
	descripcion = models.CharField(max_length=260)
	#se deben agregar los siguientes campos para realizar los calculos en otras unidades monetarias
	# vdolar = models.FLoatField() #valor del dolar 
	# vuf    = models.FLoatField() #valor de la unidad de fomento
	# fentega = fecha de entrega del proyecto
	# fconsul = fechas de consultas al cliente
	
	
class PartidasM(models.Model):
	codp  = models.IntegerField() #codigo unico que identifica y relacionara la partida(puede ser una combinacion del id automatico más el codigo para evitar multiplicidad
	nomb  = models.CharField(max_length=100,blank=None, null=None) # nombre de la partida
	desc  = models.CharField(max_length=1000) # descripcion de la partida
	unid  = models.CharField(max_length=4) # unidad de medida de la partida, puede ser kg, gr, lts, und, etc
	cost  = models.FloatField( default = 0.0 ) # costo por unidad de medida

class PartidaDetallesM(models.Model):
	# Aca se almacenan los productos, materiales o ,herramientas que pertenecen a una partidad determinada

	idpart = models.IntegerField(blank=None, null=None)#identificador de la partida a la cual pertenece este elemento
	# ~ codi = models.ForeignKey("mate.InsumosM", on_delete=models.CASCADE)
	idism = models.IntegerField()#identificador del material o insumo
	cant = models.FloatField() #cantidad del material



class Archivos(models.Model):
	TIPO=(
        ('PLNO', 'Plano'),
        ('EETT', 'Especificaciones Técnicas'),
        ('ESUE', 'Estudio de Suelo'),
        ('BAGE', 'Bases Administrativas Generales'),
        ('BAES', 'Bases Administrativas Especficas'),
        ('OTRA', 'Documento de Especificado')
    )
	idproy = models.IntegerField()
	tipo   = models.CharField(max_length=4,  choices=TIPO)
	# Los posibles valores son:
	# PLANO(planos), EETT(especificaciones tecnicas), EEOO(especificaciones de obras civiles), 
	# ESUE(estudio de Suelo), BAGE(bases administrativas generales), BAES(bases administrativas especiales)""" """
	descrip1 = models.CharField(max_length=60,blank=True, null=True)
	archivo1 = models.FileField(upload_to='Descargas/',blank=True, null=True)

class Partida(models.Model):

	idproy = models.IntegerField()
	item   = models.CharField(max_length=6)
	part   = models.CharField(max_length=100,blank=None, null=None)
	desc   = models.CharField(max_length=1000)
	unid   = models.CharField(max_length=4)
	cant   = models.IntegerField()

class DetallePartida(models.Model):
	# TIPO_ELEMENTO = (
	# 	('1','MATERIALES'),
	# 	 ('2','PERSONAL'),
	# 	 ('3','MAQyHERR'),
	# 	 ('4','SERVICIOS'),
	# 	 )

	idpart = models.IntegerField()#identificador de la partida a la cual pertenece este elemento
	idtipo = models.IntegerField()#identificador del tipo de elemento(MATERIALES:1, PERSONAL:2...)
	codi   = models.CharField(max_length=16)# identifica los materiales (materiales, maquinarias, servicio,etc)
	cant   = models.FloatField() #cantidad 
	costo  = models.FloatField()#costo unitario



class Materiales(models.Model):
	codi = models.CharField(max_length=16)
	desc = models.CharField(max_length=60)
	unid = models.CharField(max_length=4)
	cost = models.FloatField()



class Personal(models.Model):
	codi = models.CharField(max_length=4)#Acronimo de 4 letras para identificar el cargo, Ej: MM, maestro mayor
	espc = models.CharField(max_length=40)#especialidad, Electrcidad, mecanica, etc
	desc = models.CharField(max_length=60)#funciones del cargo
	cost = models.FloatField()#costo de la hora (liquida)
	#unid = model.CharField(max_length=4)# 	




