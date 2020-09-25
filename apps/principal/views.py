import os, shutil
from django.conf import settings
from datetime import datetime
import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from apps.clientes.models import ClientesM
from apps.partida.models import PartidasM
from apps.prod.models import ProductosM
from apps.ventas.models import VentasM
from apps.mate.models import InsumosM

# Create your views here.

@login_required(login_url='/inicio/ingreso')
def inicio(request):
	datos=[]
	for i in VentasM.objects.filter(estado="EN_PRO"):
		producto = ProductosM.objects.get(id=i.idprod)
		cliente  = ClientesM.objects.get(id=i.idclie)
		estado="Sin ESTADO"
		if i.estado == 'EN_PRO':
			estado = "EN PROCESO"
		if i.estado == 'EN_RUT':
			estado = "EN RUTA"
		if i.estado == 'ENTREG':
			estado = "ENTREGADO"
		print(i.estado)
		datos.append( {
					'idclie'   : cliente.id,
					'idprod'   : producto.id,
					'cliente'  : cliente.nombre,
					'nprod'    : producto.nomb,
					'telefono' : cliente.telefono,
					'cantidad' : i.cant, 
					'direccion': i.direc,
					'fhentr'   : i.fhentr,
					'dias'    : i.dias(),
					'estado'    : estado,
					})
	contexto = {
		'num_clientes'        : ClientesM.objects.count(),
		'num_partidas'        : PartidasM.objects.count(),
		'num_productos'       : ProductosM.objects.count(),
		'num_ventas'          : VentasM.objects.count(),
		'num_insumos'         : InsumosM.objects.filter(tipo="ING").count(),
		'num_materiales'      : InsumosM.objects.filter(tipo="MAT").count(),
		'num_personal'        : InsumosM.objects.filter(tipo="PER").count(),
		'ventas_por_entregar' : datos
	}
	return render( request, "inicio.html", contexto)

def usuario_nuevo (request):
	
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid:
			form.save()
			return redirect("")
	else:
		form = UserCreationForm()
		
	contexto = { "form": form }
	return render(request, "usuario_nuevo.html", contexto )

def usuario_ingreso(request):
	if not request.user.is_anonymous:
		return render(request,"privado.html")
		 
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return redirect('inicio_principal')
				else:
					return redirect(noactivo)
			else:
				return redirect(nousuario)
	else:
		
		form = AuthenticationForm()
		
	contexto = { "form": form }
	return render(request, "usuario_ingresar.html", contexto)

def cerrar(request):
	auth.logout(request)
	return redirect('usuario_ingreso')

def noactivo (request):
	
	return render(request, "noactivo.html")
	
def nousuario (request):
	
	return render(request, "nousuario.html")

def privado(request):
	
	usuario = request.user
	
	return (request,"privado.html", {'usuario': usuario})
