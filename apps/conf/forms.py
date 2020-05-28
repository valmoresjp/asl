from django import forms
from django.conf import settings
from apps.conf.models import CostosDescripcionM


class CostosDescripcionF(forms.ModelForm):
	class Meta:
		model = CostosDescripcionM
		fields = [
			'nombre', 
			'umedida',
			'cumedida',
		]
		labels = {
			'nombre':'NOMBRE DEL COSTO', 
			'umedida':'UNIDAD DE MEDIDA',
			'cumedida':'COSTO POR UNIDAD DE MEDIDA',
		}
		widgets = {
			'nombre' :forms.TextInput(attrs={'class':'form-control'}),
			'umedida' :forms.TextInput(attrs={'class':'form-control'}),
			'cumedida':forms.TextInput(attrs={'class':'form-control'}),
		}
