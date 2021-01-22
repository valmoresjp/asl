from django import forms
from django.conf import settings
from apps.mate.models import InsumosM, ComprasM, FacturasM


TIPO_ELEMENTO = (
		('...','Selecccionar tipo de Item...'),
		('MAT','MATERIAL'),
		('PER','PERSONAL'),
		('MYH','MAQyHERR'),
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
		('CM3','CENTIMETROS CÚBICOS'),
		('CC','CENTIMETROS CÚBICOS'),
		('KGR','KILOGRAMOS'),
		('GR' ,'Gramos'),
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
	# ~ def _hide_url_source_type(self):
    # ~ self.fields['copy_from'].widget = HiddenInput()
    # ~ source_type = self.fields['source_type']
    # ~ source_type.choices = [choice for choice in source_type.choices
                           # ~ if choice[0] != 'url']
    # ~ if len(source_type.choices) == 1:
        # ~ source_type.widget = HiddenInput()
        
        
	class Meta:
		model = InsumosM
		fields = [
			'codigo', 
			'descrip',
			'umedida',
			'cantd',
			'inven',
			'tipo',			
			'costop',
			'costot',

		]
		labels = {
			'codigo':'CODIGO DEL ITEM', 
			'descrip':'DESCRIPCIÓN DEL ITEM',
			'umedida':'UNIDAD DE MEDIDA',			
			'cantd':'CANTIDAD',
			'inven':'INVENTARIO',
			'tipo': 'TIPO',		
			'costop':'Costo del Producto',
			'costot':'Costo por Transporte',

		}
		widgets = {
			'codigo' :forms.TextInput(attrs={'class':'form-control'}),
			'descrip':forms.TextInput(attrs={'class':'form-control'}),
			'umedida':forms.Select(attrs={'class':'form-control'}, choices=UMEDIDA),			
			'cantd'  :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),			
			'inven'  :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),			
			'tipo'  : forms.Select(attrs={'class':'form-control'}, choices=TIPO_ELEMENTO ),
			'costop' :forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
			'costot' :forms.TextInput(attrs={'class':'form-control', 'type':'number', 'readonly':'readonly'}),
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
				'transp',
				'fhfactu',
				'archivo',
				'observ',
			]
		labels  = {
				'codigo' : 'Codigo de la Factura',
				'emisor' : 'Emisor de la Factura',
				'numero' : 'Numero de Factura',
				'total'  : 'Total',
				'transp' : 'Costo de Transporte',
				'fhfactu': 'Fecha',
				'observ' : 'Observaciones',
				'archivo': 'Archivo',
				
			}
		widgets = {
				'codigo' : 	forms.TextInput(attrs={'class':'form-control'}),
				'emisor' :  forms.TextInput(attrs={'class':'form-control','placeholder':'Local o empresa que emite la factura'}),
				'numero' :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'total'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'transp'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'fhfactu':	forms.DateInput(attrs={'class':'form-control','placeholder':'dd-mm-año'}),
				'archivo': 	forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
				'observ': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese las observaciones necesarias..'}),
			}

class PersonalF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PersonalF, self).__init__(*args, **kwargs)

		self.fields['fhfactu'].widget.format = '%d-%m-%Y'
		self.fields['fhfactu'].input_formats = ['%d-%m-%Y']
		
	class Meta:
		model = FacturasM
		fields  = [
				'codigo', 
				'emisor',
				'numero',
				'total',
				'transp',
				'fhfactu',
				'archivo',
				'observ',
			]
		labels  = {
				'codigo' : 'Codigo del Contrato',
				'emisor' : 'emisor',
				'numero' : 'numero',
				'total'  : 'Salario Liquido Acordado',
				'transp' : '',#'Salario Bruto',
				'fhfactu': 'Fecha de Contrato',
				'observ' : 'Observaciones',
				'archivo': 'Adjuntar Contrato',
				
			}
		widgets = {
				'codigo' : 	forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
				'emisor' :  forms.TextInput(attrs={'class':'form-control'}),#, 'style':"display:none;"}),
				'numero' :	forms.TextInput(attrs={'class':'form-control', 'type':'number',}),# 'style':"display:none;"}),
				'total'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'transp'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),#, 'style':"display:none;"}),
				'fhfactu':	forms.DateInput(attrs={'class':'form-control','placeholder':'dd-mm-año'}),
				'archivo': 	forms.FileInput(attrs={'class':'form-control', 'requeride':False, 'multiple': False}),
				'observ': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese las observaciones necesarias..'}),
			}
			
class ComprasF(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ComprasF, self).__init__(*args, **kwargs)
		c=[(0,'Seleccione una Factura..')]
		for i in FacturasM.objects.all().order_by('fhfactu'):
			c.append((i.id,str(i.fhfactu) +"__"+ str(i.numero)))
		
		self.fields['idfactu'].widget.choices = tuple(c)
		
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
				'costop',
				'costot',
				'cantd',
				'idfactu',
				'fhcomp',
				# ~ 'archivo'
			]
		labels = {
				'idinsm': 'ID del Insumo',
				'umedida':'Unidad de Medida',
				'costop':'Costo del Producto',
				'costot':'Costo del Transporte',
				'cantd':'Cantidad',
				'idfactu':'Numero de Factura',
				'fhcomp':'Fecha de Compra',
			}
		widgets = {
				'idinsm' : 	forms.Select(attrs={'class':'form-control'}),
				'umedida':	forms.TextInput(attrs={'class':'form-control'}),	
				'costop'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'costot'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'cantd'  :	forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
				'idfactu' :	forms.Select(attrs={'class':'form-control'}),
				'fhcomp' :	forms.DateInput(attrs={'class':'form-control','placeholder':'dd-mm-año'}),#, 'type':'date'}),
			}
