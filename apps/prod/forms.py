# -*- coding: utf-8 -*-
from django import forms
from PIL import Image
#from apps.partida.models  import Cliente, Archivos, 
from apps.prod.models import ProductosM, ImagenesM#, VentasM
from apps.clientes.models import ClientesM

def Clientes():
	c=[(0,'Seleccione un Cliente..')]
	clientes = ClientesM.objects.all()
	for i in clientes:
		c.append((i.id,i.nombre))
	return tuple(clientes)
	
class ProductosF(forms.ModelForm):
	class Meta:
		model = ProductosM
		fields =[
			'nomb',
			'codp',
			'desc',
			'unid',
			# ~ 'costo',
			# ~ 'fhcrea',
			# ~ 'fhactu',
			# ~ 'fhentr',
		]
		labels = {
			'nomb': 'Nombre',  
			'codp': 'Codigo',
			'desc': 'Descripción',
			'unid': 'Unidad de Medida',
			# ~ 'costo': 'Costo',
			# ~ 'fhcrea': 'Creación',
			# ~ 'fhactu': 'Actualizacion',
			# ~ 'fhentr': 'Entrega',
		}
		widgets = {
			'nomb'  : forms.TextInput(attrs={'class':'form-control'}),
			'codp'  : forms.TextInput(attrs={'class':'form-control'}),
			'desc'  : forms.Textarea(attrs={'class':'form-control'}),
			'unid'  : forms.TextInput(attrs={'class':'form-control'}),
			
			# ~ 'costo'  : forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'fhcrea': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'fhactu': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'fhentr': forms.DateInput(format='%d/%m/%Y ', attrs={'class': 'form-control datepicker','autocomplete': 'off'}),
			# ~ 'fhentr': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'dd-mm-año hora24:minuto'}),
		}

class ImagenesF(forms.ModelForm):
	class Meta:
		model = ImagenesM
		fields =[
			'idprod',
			'img1',
			'img2',
			'img3',
			'img4',
		]
		labels = {
			'idprod':'ID Producto',
			'img1': 'Imagen 1',
			'img2': 'Imagen 2',
			'img3': 'Imagen 3',
			'img4': 'Imagen 4',
		}
		widgets = {
			'idprod': forms.TextInput(attrs={'class':'form-control'}),
			'img1'  : forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
			'img2'  : forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
			'img3'  : forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
			'img4'  : forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),	
		}

