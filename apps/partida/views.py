import os, shutil
from django.conf import settings
from datetime import datetime
import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from apps.mate.forms import InsumosF
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM, PartidaDetallesM
from apps.partida.forms import PartidasF, PartidaDetallesF
from django.contrib.auth.decorators import login_required

#from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

def inicio(request):
	# ~ print('Pagina de Inicio')
	registro = PartidasM.objects.values()
	obj = PartidasM.objects.all()

	contexto = {
				'obj': obj,
	            }

	return render (request,'inicio_partida.html', contexto)

@login_required(login_url='/inicio/ingreso')
def nuevo(request):
	# ~ print("Nuevo")
	if request.method == 'POST':
		#form = Proyecto(request.POST, request.FILES or None)
		form = PartidasF(request.POST)
		# ~ print(request.POST)
		# ~ print(form)
		if form.is_valid():
			form.save()
			# ~ print("Guardada Nueva partida")
		else:
			# ~ print(" No se almaceno el formulario. Error!!")
			# ~ print(form)
			return render(request,'errores.html',{'form': form})
			# fh = request.POST['fecha'].replace(" ","_").replace(":","").replace("-","")[0:15]
			# cliente = request.POST.get('cliente').upper()

		#return redirect ('/proyectos/')
		# datos = {'fecha':fh, 'clien			'codp': forms.TextInput(attrs={'class':'form-control'}),te':cliente }
		# print(datos)
		return redirect ('inicio_partida')
	else:
		# ~ print("ingresando a nueva partida")
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
	# ~ print(reg.nomb)
	return render(request, 'eliminar_partida.html',{'reg':reg})

@login_required(login_url='/inicio/ingreso')
def detallar(request, idpart):
	contexto = {}
	datos = []

	if request.method =='POST':

		for i in json.loads(request.POST["ObjDatos"]):
			# ~ print(i)
			if i['destino'] == "Partidas":
				if i["accion"] == "actualizar":
					instance = PartidaDetallesM.objects.filter(idism=i["id"]).update(cant=i["datos"])
				if i["accion"] == "nuevo":
					g = PartidaDetallesM(idism=i["id"], idpart=idpart, cant=i["datos"])
					g.save()
				if i["accion"] == "eliminar":
					PartidaDetallesM.objects.filter(idpart=idpart).filter(id=i["id"]).delete()
		total = 0.0
		# ~ for k in PartidasM.objects.all():
			# ~ print(k.id)
		for i in PartidaDetallesM.objects.filter(idpart=idpart):
			if InsumosM.objects.filter(id=i.idism).exists() == True:
				ism   = InsumosM.objects.get(id=i.idism)
				total = total +  ism.cumedida()*i.cant
		ss = PartidasM.objects.filter(id=idpart).update(cost=round(total,2))
		total=0.0

		url = "/partidas/detallar/" + str(idpart) + "/"
		# ~ print(url)
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

	# ~ agregar el formset a la variable contexto
	# ~ contexto['formset'] = formset)
	# ~ print(datos)
	contexto['datos'] = datos
	contexto['partida'] = PartidasM.objects.get(id=idpart)
	contexto['insumos'] = InsumosM.objects.all()
	contexto['total'] = round(total,2)
	return render(request,'detallar_partida.html',contexto)

# ~ def agregar(request,codp, codi):
	# ~ partida = PartidasM.objects.get(id=codp)
	# ~ insumo  = InsumosM.objects.get(id=codi)
	# ~ form = PartidaDetallesF({'codp': codp, 'codi': codi, 'cant': 1.0})
	# ~ if form.is_valid():
		# ~ temp = form.save(commit=False)


	# ~ url_ant = "/detallar/" + str(codp) +"/"
	# ~ print("agregar insumo")
	# ~ codi = codi
	# ~ cant = 1.0
	# ~ cmin = insumo.min()
	# ~ cmax = insumo.max()
	# ~ cprom = insumo.prom()
	# ~ print([cmin, cmax, cprom])

	# ~ return render(request,'itemizado-1.html')

