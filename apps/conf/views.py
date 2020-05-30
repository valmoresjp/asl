from django.shortcuts import render, redirect
from apps.conf.models import CostosDescripcionM
from apps.conf.forms import CostosDescripcionF

from django.contrib.auth.decorators import login_required

# Create your views here.
def inicio(request):

	# ~ registro = ProductosM.objects.values()
	obj = CostosDescripcionM.objects.all()
	contexto = {
				'registro': obj,
	            }
	
	return render (request,'inicio_conf.html',contexto)

@login_required(login_url='/inicio/ingreso')
def agregar(request):

	if request.method == 'POST':
		form = CostosDescripcionF(request.POST)
		if form.is_valid():
			form.save()
		else:
			return render(request,'errores.html',{'form': form})
		return redirect ('inicio_conf')
	else:

		form = CostosDescripcionF()
	return render( request, 'agregar_conf.html', {'form':form})

@login_required(login_url='/inicio/ingreso')
def editar(request, idconf):
	configuracion = CostosDescripcionM.objects.get(id=idconf)
	if request.method == 'GET':
		form = CostosDescripcionF(instance=configuracion)
	else:
		form = CostosDescripcionF(request.POST, instance=configuracion)
		if form.is_valid():
			form.save()
		return redirect('inicio_conf') 
	return render(request,'agregar_conf.html', {'form':form})

@login_required(login_url='/inicio/ingreso')
def eliminar(request, idconf):
	
	# ~ print("Eliminando registro",idconf)
	if request.method == 'POST':
		url_ant = "inicio_conf"
		reg = CostosDescripcionM.objects.get(id=idconf)
		reg.delete()
		return redirect(url_ant)
	else:
		reg = CostosDescripcionM.objects.get(id=idconf)
	
	contexto = {
				'reg': reg
				}
				
	return render(request, 'eliminar_conf.html',contexto)
