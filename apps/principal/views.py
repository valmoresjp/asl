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
# Create your views here.

@login_required(login_url='/inicio/ingreso')
def inicio(request):
	
	return render( request, "inicio.html")

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
	# ~ print("cerrando... sesion")
	# ~ logout(request)
	auth.logout(request)
	return redirect('usuario_ingreso')

def noactivo (request):
	
	return render(request, "noactivo.html")
	
def nousuario (request):
	
	return render(request, "nousuario.html")


def privado(request):
	
	usuario = request.user
	
	return (request,"privado.html", {'usuario': usuario})
