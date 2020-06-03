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
	)
	
	REFER = (
		('UMED','UNIDAD/MEDIDA'),
		('TINS','INSUMOS'),
		('TMAT','MATERIALES'),
		('TIMA','INSUMOS+MATERIALES')
	)
	
	nombre = models.CharField(max_length=24, null=True, blank=True)
	umedida = models.CharField(max_length=12, choices=UMEDIDA, default='%')
	cumedida  =  models.FloatField(default=0.00)
	referencia = models.CharField(max_length=10, choices=REFER, default='INSUMOS+MATERIALES')


