# -*- coding: utf-8 -*-
from django import forms
#from apps.partida.models  import Cliente, Archivos, 
from apps.partida.models import PartidasM, PartidaDetallesM


# ~ class Proyecto(forms.ModelForm):
	# ~ class Meta:
		# ~ model = Cliente
		# ~ fields = [
			# ~ 'fecha', 
			# ~ 'cliente',  
			# ~ 'proyecto',
			# ~ 'descripcion',
			# ~ #'archivos',  
		# ~ ]
		# ~ labels = {
			# ~ 'fecha': 'Fecha', 
			# ~ 'cliente': 'Cliente',  
			# ~ 'proyecto': 'Proyecto',
			# ~ 'descripcion': 'Descripcion',
			# ~ #'archivos': 'Seleccionar Archivos', 
		# ~ }
		# ~ widgets = {
			# ~ 'fecha': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'cliente': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'proyecto': forms.TextInput(attrs={'class':'form-control'}),
			# ~ 'descripcion': forms.Textarea(attrs={'class':'form-control', 'cols':50, 'rows':3,  'maxlength':100, 'height':'10px' }),
			# ~ #'archivos': forms.TextInput(attrs={'class':'form-control'}),
			# ~ # 'archivos': forms.FileInput(attrs={'class':'form-control', 'multiple': True}),
		# ~ }

# class ArchivosM(forms.ModelForm):
	# class Meta:
		# model = Archivos
		# fields = [
			# 'idproy',
			# 'tipo',
			# 'descrip1',
			# 'archivo1',
		# ]

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
			'unid': forms.TextInput(attrs={'class':'form-control'}),
			'cost': forms.TextInput(attrs={'class':'form-control'}),
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


# class Partidas(forms.ModelForm):
	# class Meta:
		# model = Partida
		# fields =[
			# 'idproy',
			# 'item',
			# 'part',
			# 'desc',
			# 'unid',
			# 'cant',
		# ]
		# labels = {
			# 'idproy': 'Proyecto', 
			# 'item': 'Item',  
			# 'part': 'Partida',
			# 'desc': 'Descripción',
			# 'unid': 'Unidad',
			# 'cant': 'Cantidad',
			# #'archivos': 'Seleccionar Archivos', 
		# }
		# widgets = {
			# 'idproy': forms.TextInput(attrs={'class':'form-control', 'style':"visibility:hidden; height:0"}),
			# 'item': forms.TextInput(attrs={'class':'form-control'}),
			# 'part': forms.Textarea(attrs={'class':'form-control'}),
			# 'desc': forms.Textarea(attrs={'class':'form-control'}),
			# 'unid': forms.TextInput(attrs={'class':'form-control'}),
			# 'cant': forms.TextInput(attrs={'class':'form-control'}),
		# }	

# class PartidaM(forms.ModelForm):
	# class Meta:
		# model = Partida
		# fields =[
			# 'idproy',
			# 'item',
			# 'part',
			# 'desc',
			# 'unid',
			# 'cant',
		# ]
		# labels = {
			# 'idproy': 'Proyecto', 
			# 'item': 'Item',  
			# 'part': 'Partida',
			# 'desc': 'Descripción',
			# 'unid': 'Unidad',
			# 'cant': 'Cantidad',
			# #'archivos': 'Seleccionar Archivos', 
		# }
		# widgets = {
			# 'idproy': forms.TextInput(attrs={'class':'form-control', 'style':"visibility:hidden; height:0"}),
			# 'item': forms.TextInput(attrs={'class':'form-control'}),
			# 'part': forms.Textarea(attrs={'class':'form-control'}),
			# 'desc': forms.Textarea(attrs={'class':'form-control'}),
			# 'unid': forms.TextInput(attrs={'class':'form-control'}),
			# 'cant': forms.TextInput(attrs={'class':'form-control'}),
		# }
