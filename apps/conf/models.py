from django.db import models

# Create your models here.:
class CostosDescripcionM(models.Model):
	nombre = models.CharField(max_length=24, null=True, blank=True)
	umedida = models.CharField(max_length=12, null=True, blank=True)
	cumedida  =  models.FloatField(default=0.00)


