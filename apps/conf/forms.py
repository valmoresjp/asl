from django import forms
from django.conf import settings
from apps.conf.models import CostosDescripcionM

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
		('TCAD','COSTOS_ADICIONALES'),
		('TIMA','INSUMOS+MATERIALES'),
		('IMAC','INSUMOS+MATERIALES+COSTOS_ADICIONALES'),
)

class CostosDescripcionF(forms.ModelForm):
	class Meta:
		model = CostosDescripcionM
		fields = [
			'nombre', 
			'umedida',
			'cumedida',
			'referencia',
		]
		labels = {
			'nombre':'NOMBRE DEL COSTO', 
			'umedida':'UNIDAD DE MEDIDA',
			'cumedida':'COSTO POR UNIDAD DE MEDIDA',
			'referencia':'CELDA DE REFRENCIA',
		}
		widgets = {
			'nombre' :forms.TextInput(attrs={'class':'form-control'}),
			'umedida' :forms.Select(attrs={'class':'form-control'},  choices=UMEDIDA),
			'cumedida':forms.TextInput(attrs={'class':'form-control'}),
			'refrencia':forms.Select(attrs={'class':'form-control'}, choices=REFER),
		}
