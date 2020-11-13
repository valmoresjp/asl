from django.shortcuts import render,redirect
from datetime import datetime

from  apps.prod.models import ProductosM #VentasM, 
from apps.ventas.models import VentasM, ResumenM
from apps.clientes.models import ClientesM
from apps.clientes.forms import ClientesF

# Create your views here.

def inicio(request):
	clientes = ClientesM.objects.all().order_by('-id')
	
	contexto = {
				'clientes': clientes,
	           }
	return render(request, "inicio_cliente.html", contexto)

# ~ @login_required(login_url='/inicio/ingreso')
def agregar(request):

	if request.method == 'POST':
		form = ClientesF(request.POST)
		if form.is_valid():
			instancia = form.save(commit=False)
			instancia.nombre = (instancia.nombre).upper()
			form.save()
			# ~ print("Creando nuevo cliente")
			## almacenar datos en la tabla ResumenM
			t = datetime.now()
			ayo  = t.year
			mes  =  t.month
			clientes_totales = ClientesM.objects.filter(fhreg__year = ayo).count()
			num_clientes = ClientesM.objects.filter(fhreg__year=ayo, fhreg__month=mes).count()
			# ~ r = ResumenM.objects.filter(ayo = ayo).filter(mes = mes)
			if ResumenM.objects.filter(ayo = ayo).filter(mes = mes).exists():
				ResumenM.objects.filter(ayo = ayo, mes = mes).update(ncli_n=num_clientes, ncli_t=clientes_totales)
			else:
				a = ResumenM(ayo=ayo, mes=mes, ncli_n=num_clientes, ncli_t=clientes_totales)
				a.save()
		else:
			return render(request,'errores.html',{'form': form})

		return redirect ('inicio_clientes')
	else:
		form = ClientesF()
		contexto = {
					'form':form,
					'nombres': ClientesM.objects.all().order_by('nombre')
					}
	return render(request,'agregar_cliente.html', contexto)
	
# ~ @login_required(login_url='/inicio/ingreso')
def editar(request, idclie ):
	clientes = ClientesM.objects.get(id=idclie)
	if request.method == 'GET':
		form = ClientesF(instance=clientes)
	else:
		form = ClientesF(request.POST, instance=clientes)
		if form.is_valid():
			form.save()
		else:
			return render(request,'errores.html',{'form': form})
		return redirect('inicio_clientes') 
	return render(request,'agregar_cliente.html', {'form':form})

# ~ @login_required(login_url='/inicio/ingreso')
def detallar(request, idclie ):
	total = 0.0
	vdatos = []
	cliente = ClientesM.objects.get(id=idclie)
	
	for i in VentasM.objects.filter(idclie = idclie).order_by('-fhacd', 'fhentr'):
		prod  = ProductosM.objects.get(id=i.idprod)
		vdatos.append ({
				'id'    : i.id,
				'idclie': idclie,
				'idprod': prod.id,
				'nprod' : prod.nomb,
				'cant'  : i.cant,
				'costo' : i.costo,
				'obsrv' : i.obsrv,
				'direc' : i.direc,
				'centr' : i.centr,
				'fhacd' : i.fhacd,
				'fhentr': i.fhentr,
				'estado': i.estado_producto(),
				'estado_n' : i.estado,
				})
		total = total + i.costo
			
	contexto = {
				'cliente': cliente,
				'vdatos': vdatos,
				'total': round(total,2)
	           }
	return render(request,'detallar_cliente.html', contexto)
