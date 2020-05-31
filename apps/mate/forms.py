from django import forms
from django.conf import settings
from apps.mate.models import InsumosM


TIPO_ELEMENTO = (
		('..','Selecccionar...'),
		('MAT','MATERIAL-'),
		('PER','PERSONAL'),
		('MYH','MAQyHERR'),
		('SER','SERVICIO'),
		('ING','INGREDIENTE'),
	)	

class InsumosF(forms.ModelForm):
	class Meta:
		model = InsumosM
		fields = [
			'codigo', 
			'fingso',
			'descrip',
			'umedida',
			'cantd',
			'inven',
			'tipo',			
			'distb1',
			'costo1',
			# ~ 'cantm1',
			'factu1',			
			'distb2',
			'costo2',
			# ~ 'cantm2',
			'factu2',			
			'distb3',
			'costo3',
			# ~ 'cantm3',
			'factu3',
			'distb4',
			'costo4',
			# ~ 'cantm4',
			'factu4',
			'distb5',
			'costo5',
			# ~ 'cantm5',
			'factu5'
		]
		labels = {
			'codigo':'CODIGO DEL PRODUCTO', 
			'fingso':'FECHA DE INGRESO DEL REGISTRO',
			'descrip':'DESCRIPCIÓN DEL PRODUCTO',
			'umedida':'UNIDAD DE MEDIDA',			
			'cantd':'CANTIDAD',
			'inven':'INVENTARIO',
			'tipo': 'TIPO',		
			'distb1':'DISTRIBUIDOR 1',
			'costo1':'COSTO 1',
			# ~ 'cantm1':'CANTIDAD MINIMA',
			'factu1':'FECHA DE INGRESO',			
			'distb2':'DISTRIBUIDOR 2',
			'costo2':'COSTO 2',
			# ~ 'cantm2':'CANTIDAD MINIMA',
			'factu2':'FECHA DE INGRESO',			
			'distb3':'DISTRIBUIDOR 3',
			'costo3':'COSTO 3',
			# ~ 'cantm3':'CANTIDAD MINIMA',
			'factu3':'FECHA DE INGRESO',
			'distb4':'DISTRIBUIDOR 4',
			'costo4':'COSTO 4',
			# ~ 'cantm4':'CANTIDAD MINIMA',
			'factu4':'FECHA DE INGRESO',
			'distb5':'DISTRIBUIDOR 5',
			'costo5':'COSTO 5',
			# ~ 'cantm5':'CANTIDAD MINIMA',
			'factu5':'FECHA DE INGRESO'
		}
		widgets = {
			'codigo' :forms.TextInput(attrs={'class':'form-control'}),
			'fingso' :forms.TextInput(attrs={'class':'form-control'}),
			'descrip':forms.TextInput(attrs={'class':'form-control'}),
			'umedida':forms.TextInput(attrs={'class':'form-control'}),			
			'cantd'  :forms.TextInput(attrs={'class':'form-control'}),			
			'inven'  :forms.TextInput(attrs={'class':'form-control'}),			
			'tipo'  : forms.Select(attrs={'class':'form-control'}, choices=TIPO_ELEMENTO ),
						
			'distb1' :forms.TextInput(attrs={'class':'form-control'}),
			'costo1' :forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cantm1' :forms.TextInput(attrs={'class':'form-control'}),
			'factu1' :forms.TextInput(attrs={'class':'form-control'}),
			
			'distb2' :forms.TextInput(attrs={'class':'form-control'}),
			'costo2' :forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cantm2' :forms.TextInput(attrs={'class':'form-control'}),
			'factu2' :forms.TextInput(attrs={'class':'form-control'}),
			
			'distb3' :forms.TextInput(attrs={'class':'form-control'}),
			'costo3' :forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cantm3' :forms.TextInput(attrs={'class':'form-control'}),
			'factu3' :forms.TextInput(attrs={'class':'form-control'}),

			'distb4' :forms.TextInput(attrs={'class':'form-control'}),
			'costo4' :forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cantm4' :forms.TextInput(attrs={'class':'form-control'}),
			'factu4' :forms.TextInput(attrs={'class':'form-control'}),

			'distb5' :forms.TextInput(attrs={'class':'form-control'}),
			'costo5' :forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cantm5' :forms.TextInput(attrs={'class':'form-control'}),
			'factu5' :forms.TextInput(attrs={'class':'form-control'})

		# 'archivos': forms.FileInput(attrs={'class':'form-control', 'multiple': True}),
		}
