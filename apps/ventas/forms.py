# -*- coding: utf-8 -*-
from django import forms
#from apps.partida.models  import Cliente, Archivos, 
from apps.ventas.models import VentasM
from apps.clientes.models import ClientesM


# ~ ESTADO = (
		# ~ ('EN_PRO','EN PROCESO'),
		# ~ ('COMPLE','COMPLETADO'),
		# ~ ('EN_RUT','EN RUTA'),
		# ~ ('ENTREG','ENTREGADO'),
	# ~ )

	
ESTADO = (
		(0,'POR APROBACION'),
		(1,'EN PROCESO'),
		(2,'EN RUTA'),
		(3,'ENTREGADO'),
	)


class VentasF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(VentasF, self).__init__(*args, **kwargs)
		c=[(0,'Seleccione un Cliente..')]
		for i in ClientesM.objects.all():
			c.append((i.id,i.nombre))
		
		self.fields['idclie'].widget.choices = tuple(c)
		self.fields['obsrv'].required = False
		self.fields['direc'].required = True
		self.fields['cant'].required = False
		self.fields['estado'].widget.choices = tuple(ESTADO)
		# ~ self.fields['estado'].widget.attrs['disabled'] = 'disabled'
		# ~ print(ESTADO(0))
		# ~ self.fields['fhentr'].input_formats = ['%d-%m-%Y %H:%M']
		# ~ self.fields['fhentr'].input_formats = ['%Y-%m-%d %H:%M']
		
	class Meta:
		model = VentasM
		fields =[
			'idprod',
			'idclie', 
			'cant',   
			'costo', 
			'pers',
			'insm', 
			'mate', 
			'serv',
			'utlds', 
			'obsrv',
			'direc',
			'centr',
			'fhentr',
			'estado',
		]
		labels = {
			'idprod' : 'ID Producto',
			'idclie' : 'Cliente',
			'cant'   : 'Cantidad',
			'costo'  : 'Costo',
			'pers'   : 'Personal',
			'insm'   : 'Insumos',
			'mate'   : 'Materiales', 
			'serv'   : 'Servicios',
			'utlds'  : 'Utilidades', 
			'obsrv'  : 'Observaciones',
			'direc'  : 'Direccion de Entrega',
			'centr'  : 'Costos de Entrega',
			'fhentr' : 'Fecha de Entrega',
			'estado' : 'Estado de Entrega',
		}
		widgets = {
			'idprod' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}),
			'idclie' : forms.Select(attrs={'class':'form-control'} ), 
			'cant'   : forms.TextInput(attrs={'class':'form-control', 'type':'number'}),   
			'costo'  : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}), 
			'pers'   : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}),
			'insm'   : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}), 
			'mate'   : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}), 
			'serv'   : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}),
			'utlds'  : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'type':'hidden'}), 
			'obsrv'  : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese las observaciones necesarias..'}),
			'direc'  : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección de entrega..'}),
			'centr'  : forms.TextInput(attrs={'class':'form-control'}),
			'fhentr' : forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'estado' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'value':'1'}),
			'estado' : forms.Select(attrs={'class':'form-control ocultar', 'readonly':'readonly', 'type':'hidden'} ), 
		}
