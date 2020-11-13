# -*- coding: utf-8 -*-
from django import forms
from apps.clientes.models import ClientesM

class ClientesF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ClientesF, self).__init__(*args, **kwargs)
		self.fields['fhaniver'].widget.format = '%d-%m-%Y'
		self.fields['fhaniver'].input_formats = ['%d-%m-%Y']

		# ~ c=[(0,'Escriba el nombre completo del cliente..')]
		# ~ for i in ClientesM.objects.all().order_by('nombre'):
			# ~ c.append((i.id,str(i.nombre)))
		
		# ~ self.fields['nombre'].widget.choices = tuple(c)

			
	class Meta:
		model = ClientesM
		fields =[
			'nombre',
			'telefono',
			'correo',
			'fhaniver',
		]
		labels = {
			'nombre'  : 'Nombres y Apellidos',  
			'telefono': 'Número Telefónico',
			'correo'  : 'Correo Electronico',
			'fhaniver': 'Fecha d Aniversario',
		}
		widgets = {
			# ~ 'nombre'  : forms.Select(attrs={'class':'form-control'}),
			'nombre'  : forms.TextInput(  attrs={'class':'form-control', 'list':'nombre', 'placeholder':'Escriba el nombre que sera agregado...'}),
			'telefono': forms.TextInput(attrs={'class':'form-control', 'type':'tel', 'pattern':'+[0-9]{2} [0-9]{9}', 'placeholder':'ejemplo:  +56 123456789'}),
			'correo'  : forms.TextInput(attrs={'class':'form-control', 'type':'email', 'placeholder':'ejemplo: tu_email@servidor.extension'}),
			'fhaniver': forms.DateInput(attrs={'class':'form-control', 'placeholder':'dd-mm-aaaa'}),
		}	
