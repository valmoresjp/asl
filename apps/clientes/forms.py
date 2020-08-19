# -*- coding: utf-8 -*-
from django import forms
from apps.clientes.models import ClientesM

class ClientesF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ClientesF, self).__init__(*args, **kwargs)
		self.fields['fhaniver'].widget.format = '%d-%m-%Y'
		self.fields['fhaniver'].input_formats = ['%d-%m-%Y']
			
	class Meta:
		model = ClientesM
		fields =[
			'nombre',
			'telefono',
			'fhaniver',
		]
		labels = {
			'nombre'  : 'Nombres y Apellidos',  
			'telefono': 'Número Telefónico',
			'fhaniver': 'Fecha d Aniversario',
		}
		widgets = {
			'nombre': forms.TextInput(  attrs={'class':'form-control'}),
			'telefono': forms.TextInput(attrs={'class':'form-control', 'type':'tel', 'pattern':'+[0-9]{2} [0-9]{9}', 'placeholder':'+56 123456789'}),
			'fhaniver': forms.DateInput(attrs={'class':'form-control', 'placeholder':'dd-mm-aaaa'}),
		}	
