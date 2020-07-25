# -*- coding: utf-8 -*-
from django import forms
from apps.partida.models import PartidasM, PartidaDetallesM


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

class PartidasF(forms.ModelForm):
	class Meta:
		model = PartidasM
		fields =[
			'codp',
			'nomb',
			'desc',
			'unid',
			'cost',
		]
		labels = {
			'codp': 'Codigo de la Partida', 
			'nomb': 'Nombre',  
			'desc': 'Descripción',
			'unid': 'Unidad de Medida',
			'cost': 'Costo',
			#'archivos': 'Seleccionar Archivos', 
		}
		widgets = {
			#'codp': forms.TextInput(attrs={'class':'form-control', 'style':"visibility:hidden; height:0"}),
			'codp': forms.TextInput(attrs={'class':'form-control'}),
			'nomb': forms.TextInput(attrs={'class':'form-control'}),
			'desc': forms.Textarea(attrs={'class':'form-control'}),
			'unid': forms.Select(attrs={'class':'form-control'}, choices=UMEDIDA),
			'cost': forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
		}	

class PartidaDetallesF(forms.ModelForm):
	class Meta:
		model = PartidaDetallesM
		fields = '__all__'
		# ~ fields =[
			# ~ 'codp',
			# ~ 'codi',
			# ~ 'cant',
		# ~ ]
		# ~ labels = {
			# ~ 'codp': 'Id Partida', 
			# ~ 'codi': 'Id Insumo',  
			# ~ 'cant': 'Cantidad',
		# ~ }
		# ~ widgets = {
			# ~ #'codp': forms.TextInput(attrs={'class':'form-control', 'style':"visibility:hidden;"}),
			# ~ 'codp': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'codi': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cant': forms.TextInput(attrs={'class':'form-control'}),
		# ~ }	

