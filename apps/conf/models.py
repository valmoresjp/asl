from django.db import models

# Create your models here.:
class CostosDescripcionM(models.Model):
	
	UMEDIDA =(
		('%'  ,'PORCENTAJE'),
		('Kwh','KILOVATIO-HORA'),
		('M3' ,'METROS CUBICOS'),
		('Lts','LITROS'),
		('Kgr','KILOGRAMOS'),
		('Gr' ,'Gramos'),
		('Mts','METROS'),
		('Km' ,'KILOMETROS'),
		('Und','UNIDAD'),
		('HH' ,'HORAS-HOMBRE'),
		('MES' ,'MENUSAL'),
		('DIA' ,'DIARIO'),
		('HRS' ,'HORAS'),
	)
	
	REFER = (
		('UMED','UNIDAD/MEDIDA'),
		('TINS','INSUMOS'),
		('TMAT','MATERIALES'),
		('MOBR','MANO DE OBRA'),
		('TCAD','COSTOS_ADICIONALES'),
		('TIMA','INSUMOS+MATERIALES'),
		('IMAC','INSUMOS+MATERIALES+COSTOS_ADICIONALES'),
		('IMACM','INSUMOS+MATERIALES+COSTOS_ADICIONALES+MANO_OBRA'),
	)
	TIPO = (
		('SERV','SERVICIO'),
		('INSM','INSUMO'),
		('MYHR','MAQUINA y HERRAMIENTA'),
		('PER','PERSONAL'),
	)
	
	nombre     = models.CharField(max_length=24, null=True, blank=True)
	umedida    = models.CharField(max_length=12, choices=UMEDIDA, default='%')
	cumedida   = models.FloatField(default=0.0)
	tipo       = models.CharField(max_length=4, choices=TIPO, default='SERVICIO')
	referencia = models.CharField(max_length=10, choices=REFER, default='INSUMOS+MATERIALES')

class UtilidadesM(models.Model):
	descripcion  = models.CharField(max_length=24, null=True, blank=True)
	porcentaje   = models.FloatField(default=30.0)
	
class UtilidadesDetallesM(models.Model):
	idprod     = models.IntegerField() #id del producto
	idutil     = models.IntegerField() # id del item utilidad ( tabla UtilidadesM)
	porcentaje = models.FloatField(default=0.0) #Porcentaje 
	valor      = models.FloatField(default=0.0) #valor correspondiente al porcentaje
	 
