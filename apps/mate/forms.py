from django import forms
from django.conf import settings
from apps.mate.models import InsumosM, ComprasM, FacturasM


TIPO_ELEMENTO = (
		('...','Selecccionar tipo de Item...'),
		('MAT','MATERIAL'),
		('PER','PERSONAL'),
		# ~ ('MYH','MAQyHERR'),
		('SER','SERVICIO'),
		('ING','INGREDIENTE'),
	)

UMEDIDA =(
		('..','Selecccione la unidad de medida...'),
		('%'  ,'PORCENTAJE'),
		('KWH','KILOVATIO-HORA'),
		('M3' ,'METROS CUBICOS'),
		('LTS','LITROS'),
		('ML','MILILITROS'),
		('CC','CENTIMETROS CÚBICOS'),
		('KGR','KILOGRAMOS'),
		('Gr' ,'Gramos'),
		('MTS','METROS'),
		('KM' ,'KILOMETROS'),
		('UND','UNIDAD'),
		('HH' ,'HORAS-HOMBRE'),
		('HRS','HORAS'),
		('MES','MENSUAL'),
		('DIA','DIARIO'),
		('HM' ,'HORAS-MAQUINA'),
	)	

class InsumosF(forms.ModelForm):
	class Meta:
		model = InsumosM
		fields = [
			'codigo', 
			# ~ 'fingso',
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
			'codigo':'CODIGO DEL ITEM', 
			# ~ 'fingso':'FECHA DE INGRESO DEL REGISTRO',
			'descrip':'DESCRIPCIÓN DEL ITEM',
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
			# ~ 'fingso' :forms.TextInput(attrs={'class':'form-control'}),
			'descrip':forms.TextInput(attrs={'class':'form-control'}),
			'umedida':forms.Select(attrs={'class':'form-control'}, choices=UMEDIDA),			
			'cantd'  :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),			
			'inven'  :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),			
			'tipo'  : forms.Select(attrs={'class':'form-control'}, choices=TIPO_ELEMENTO ),
						
			'distb1' :forms.TextInput(attrs={'class':'form-control'}),
			'costo1' :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
			# ~ 'cantm1' :forms.TextInput(attrs={'class':'form-control'}),
			'factu1' :forms.TextInput(attrs={'class':'form-control'}),
			
			'distb2' :forms.TextInput(attrs={'class':'form-control'}),
			'costo2' :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
			# ~ 'cantm2' :forms.TextInput(attrs={'class':'form-control'}),
			'factu2' :forms.TextInput(attrs={'class':'form-control'}),
			
			'distb3' :forms.TextInput(attrs={'class':'form-control'}),
			'costo3' :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
			# ~ 'cantm3' :forms.TextInput(attrs={'class':'form-control'}),
			'factu3' :forms.TextInput(attrs={'class':'form-control'}),

			'distb4' :forms.TextInput(attrs={'class':'form-control'}),
			'costo4' :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
			# ~ 'cantm4' :forms.TextInput(attrs={'class':'form-control'}),
			'factu4' :forms.TextInput(attrs={'class':'form-control'}),

			'distb5' :forms.TextInput(attrs={'class':'form-control'}),
			'costo5' :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
			# ~ 'cantm5' :forms.TextInput(attrs={'class':'form-control'}),
			'factu5' :forms.TextInput(attrs={'class':'form-control'})

		# 'archivos': forms.FileInput(attrs={'class':'form-control', 'multiple': True}),
		}

class FacturasF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(FacturasF, self).__init__(*args, **kwargs)

		self.fields['fhfactu'].widget.format = '%d-%m-%Y'
		self.fields['fhfactu'].input_formats = ['%d-%m-%Y']
		
	class Meta:
		model = FacturasM
		fields  = [
				'codigo', 
				'emisor',
				'numero',
				'total',
				'fhfactu',
				'archivo',
			]
		labels  = {
				'codigo' : 'Codigo de la Factura',
				'emisor' : 'Emisor de la Factura',
				'numero' : 'Numero de Factura',
				'total'  : 'Total',
				'fhfactu': 'Fecha',
				'archivo': 'Archivo',
			}
		widgets = {
				'codigo' : 	forms.TextInput(attrs={'class':'form-control'}),
				'emisor' :  forms.TextInput(attrs={'class':'form-control','placeholder':'Local o empresa que emite la factura'}),
				'numero' :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'total'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'fhfactu':	forms.DateInput(attrs={'class':'form-control','placeholder':'dd-mm-año'}),
				'archivo': 	forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
			}
			
class ComprasF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ComprasF, self).__init__(*args, **kwargs)
		c=[(0,'Seleccione una Factura..')]
		for i in FacturasM.objects.all().order_by('fhfactu'):
			c.append((i.id,str(i.fhfactu) +"__"+ str(i.numero)))
		
		
		self.fields['nfactu'].widget.choices = tuple(c)
		
		d=[(0,'Seleccione un Item..')]
		for i in InsumosM.objects.all().order_by('descrip'):
			d.append((i.id,i.descrip))
		
		self.fields['idinsm'].widget.choices = tuple(d)
		
		self.fields['fhcomp'].widget.format = '%d-%m-%Y'
		self.fields['fhcomp'].input_formats = ['%d-%m-%Y']
	
	class Meta:
		model = ComprasM
		fields = [
				'idinsm', 
				'umedida',
				'costo',
				'cantd',
				'nfactu',
				'fhcomp',
				# ~ 'archivo'
			]
		labels = {
				'idinsm': 'ID del Insumo',
				'umedida':'Unidad de Medida',
				'costo':'Costo',
				'cantd':'Cantidad',
				'nfactu':'Numero de Factura',
				'fhcomp':'Fecha de Compra',
				# ~ 'archivo':'Factura(adjuntar archivo)'
			}
		widgets = {
				'idinsm' : 	forms.Select(attrs={'class':'form-control'}),
				# ~ 'idinsm' : 	forms.TextInput(attrs={'class':'form-control'}),
				# ~ 'umedida':	forms.Select(attrs={'class':'form-control'}, choices=UMEDIDA),	
				'umedida':	forms.TextInput(attrs={'class':'form-control'}),	
				'costo'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'cantd'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'nfactu' :	forms.Select(attrs={'class':'form-control'}),
				# ~ 'nfactu' :	forms.TextInput(attrs={'class':'form-control'}),
				'fhcomp' :	forms.DateInput(attrs={'class':'form-control','placeholder':'dd-mm-año'}),#, 'type':'date'}),
				# ~ 'archivo': 	forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
			}
