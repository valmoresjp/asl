# ~ import os, shutil
# ~ from django.conf import settings
# ~ from datetime import datetime
import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

# ~ from apps.mate.forms import InsumosF
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM, PartidaDetallesM
# ~ from apps.partida.forms import PartidasF, PartidaDetallesF
from django.contrib.auth.decorators import login_required

#from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

def inicio(request):
	# ~ print('Pagina de Inicio')
	# ~ registro = PartidasM.objects.values()
	obj = PartidasM.objects.all()
	
	contexto = {
				'obj': obj,
	            }
	
	return render (request,'inicio_partida.html', contexto)

@login_required(login_url='/inicio/ingreso')
def nuevo(request):
	if request.method == 'POST':
		form = PartidasF(request.POST)
		if form.is_valid():
			form.save()

		else:
			return render(request,'errores.html',{'form': form})

		return redirect ('inicio_partida')
	else:
		form = PartidasF()
	return render(request,'nuevo_partida.html', {'form': form})

@login_required(login_url='/inicio/ingreso')
def editar(request, idpart):
	partidas = PartidasM.objects.get(id=idpart)
	if request.method == 'GET':
		form = PartidasF(instance=partidas)
	else:
		form = PartidasF(request.POST, instance=partidas)
		if form.is_valid():
			form.save()
		return redirect('inicio_partida') 
	return render(request,'nuevo_partida.html', {'form':form})

@login_required(login_url='/inicio/ingreso')
def eliminar(request, idpart):

	if request.method == 'POST':
		url_ant = "inicio_partida"
		reg = PartidasM.objects.get(id=idpart)
		#se deben eliminar los registros de materiales pertenecientes a esta partida
		# estos están ubicados en la tabla "PartidaDetallesM"
		for i in PartidaDetallesM.objects.filter(idpart=reg.id):
			i.delete()
		reg.delete()
		return redirect(url_ant)
	else:
		reg = PartidasM.objects.get(id=idpart)

	return render(request, 'eliminar_partida.html',{'reg':reg})

@login_required(login_url='/inicio/ingreso')
def detallar(request, idpart):
	contexto = {}
	datos = []
	
	if request.method =='POST':
		for i in json.loads(request.POST["ObjDatos"]):
			if i['destino'] == "Partidas":
				if i["accion"] == "actualizar":
					PartidaDetallesM.objects.filter(idism=i["id"]).update(cant=i["datos"])
				if i["accion"] == "nuevo":
					g = PartidaDetallesM(idism=i["id"], idpart=idpart, cant=i["datos"])
					g.save()					
				if i["accion"] == "eliminar":
					PartidaDetallesM.objects.filter(idpart=idpart).filter(id=i["id"]).delete()			
		total = 0.0
		for i in PartidaDetallesM.objects.filter(idpart=idpart):
			if InsumosM.objects.filter(id=i.idism).exists() == True:
				ism   = InsumosM.objects.get(id=i.idism)
				total = total +  ism.cumedida()*i.cant
		PartidasM.objects.filter(id=idpart).update(cost=round(total,2))
		total=0.0
		
		url = "/partidas/detallar/" + str(idpart) + "/"
		return redirect(url)
		
	if request.method == 'GET':

		total = 0.0
		for i in PartidaDetallesM.objects.filter(idpart=idpart):
			ism   = InsumosM.objects.get(id=i.idism)
			datos.append(	
					{'pdm_id':     i.id, 
					 'pdm_codi':   i.idism,
					 'pdm_codp':   i.idpart,
					 'pdm_cant':   i.cant,
					 'ism_id':     ism.id,
					 'ism_codigo': ism.codigo,
					 'ism_descrip': ism.descrip,
					 'ism_umedida': ism.umedida,
					 'ism_costo':   ism.cumedida(),
					 'ism_total':   round(ism.cumedida()*i.cant,2)
					 })
			total = total +  ism.cumedida()*i.cant
			
	contexto['datos'] = datos 
	contexto['partida'] = PartidasM.objects.get(id=idpart)
	contexto['insumos'] = InsumosM.objects.all()
	contexto['total'] = round(total,2)
	return render(request,'detallar_partida.html',contexto)
