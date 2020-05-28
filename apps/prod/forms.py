# -*- coding: utf-8 -*-
from django import forms
#from apps.partida.models  import Cliente, Archivos, 
from apps.prod.models import ProductosM, ProductosDetallesM


# ~ class ProductosDetallesM(models.Model):
	# ~ idpart = models.IntegerField() #id de la partida
	# ~ unidad = models.IntegerField() # unidad de medida
	# ~ cantid = models.FloatField() #cantidad
	# ~ item   = models.CharField(max_length=6)
	# ~ costo  = models.FloatField()  #costo en pesos chilenos 


class ProductosF(forms.ModelForm):
	class Meta:
		model = ProductosM
		fields =[
			'nomb',
			'codp',
			'desc',
			'unid',
		]
		labels = {
			'nomb': 'Nombre',  
			'codp': 'Codigo',
			'desc': 'Descripción',
			'unid': 'Unidad de Medida',
		}
		widgets = {
			'nomb': forms.TextInput(attrs={'class':'form-control'}),
			'codp': forms.TextInput(attrs={'class':'form-control'}),
			'desc': forms.Textarea(attrs={'class':'form-control'}),
			'unid': forms.TextInput(attrs={'class':'form-control'}),
		}	
