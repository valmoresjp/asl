from django.shortcuts import render, redirect
import json
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM, PartidaDetallesM
from apps.prod.models import ProductosM, ProductosDetallesM, MaquiyHerraM, CstsAdnlsM
from apps.conf.models import CostosDescripcionM
from apps.prod.forms import ProductosF
from django.db.models import Q

from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):

	# ~ registro = ProductosM.objects.values()
	obj = ProductosM.objects.all()
	contexto = {
				'obj': obj,
	            }
	
	return render (request,'inicio_producto.html', contexto)

@login_required(login_url='/inicio/ingreso')
def nuevo(request):
	print("Nuevo")
	if request.method == 'POST':
		form = ProductosF(request.POST)
		if form.is_valid():
			form.save()
		else:
			return render(request,'errores.html',{'form': form})

		return redirect ('inicio_producto')
	else:
		# ~ print("ingresando a nuevo_producto")
		form = ProductosF()
	return render(request,'nuevo_producto.html', {'form': form})

@login_required(login_url='/inicio/ingreso')
def editar(request, idprod ):
	producto = ProductosM.objects.get(id=idprod)
	if request.method == 'GET':
		form = ProductosF(instance=producto)
	else:
		form = ProductosF(request.POST, instance=producto)
		if form.is_valid():
			form.save()
		return redirect('inicio_producto') 
	return render(request,'nuevo_producto.html', {'form':form})

@login_required(login_url='/inicio/ingreso')
def eliminar(request, idprod):

	if request.method == 'POST':
		url_ant = "inicio_producto"
		reg = ProductosM.objects.get(id=idprod)
		reg.delete()
		return redirect(url_ant)
	else:
		reg = ProductosM.objects.get(id=idprod)
	
	return render(request, 'eliminar_producto.html',{'reg':reg})
	
def detallar(request, idprod):
	print("INGRESANDO A DETALLAR: ", idprod)
	contexto = {}
	idatos = []
	mdatos = []
	cdatos = []
	udatos = []
	totales = { 'totprd':0.0, 'prddetlls':0.0, 'maqyherr': 0.0, 'cstsadnls': 0.0 }
	totprd = 0.0
	total = 0.0

	producto   = ProductosM.objects.get(id=idprod)
	# ~ materiales = MaquiyHerraM.objects.all()
	partida    = PartidaDetallesM.objects.all()
	# ~ prd_deta   = ProductosDetallesM.objects.filter(idprd=idprod)

	if request.method =='POST':
		# ~ print("DETALLAR: metodo POST")
		url = "/productos/detallar/" + str(idprod) + "/"
		# ~ print(url)
		print(request.POST['ObjDatos'])
		for i in json.loads(request.POST["ObjDatos"]):
			
			if i['destino'] == "Insumos":
				if i['accion'] == 'actualizar':
					# ~ res = ProductosDetallesM.objects.filter(idprd=idprod).filter(idpart=i["id"]).exists()
					# ~ print("El registro existe y se actualizara")
					# ~ print(i["id"],"   ",i["datos"])
					ProductosDetallesM.objects.filter(idpart=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ print("el registro no existe y se agregara")
					# ~ print(i)
					# ~ El registro no existe, se crea un nuevo registro
					g = ProductosDetallesM(idpart=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
					ProductosDetallesM.objects.filter(id=i["id"]).delete()
					
			if i['destino'] == "Materiales":
				if i['accion'] == 'actualizar':
					# ~ El registro existe y se actualiza
					MaquiyHerraM.objects.filter(idism=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = MaquiyHerraM(idism=i["id"], idprd=idprod, cant=i["datos"])
					g.save()					
				if i['accion'] == 'eliminar':
					MaquiyHerraM.objects.filter(idprd=idprod).filter(idism=i["id"]).delete()				
				
			if i['destino'] == "CostosAdicionales":
				if i['accion'] == 'actualizar':
					# ~ El registro existe y se actualiza
					CstsAdnlsM.objects.filter(id=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = CstsAdnlsM(idcstanls=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
					CstsAdnlsM.objects.filter(id=i["id"]).delete()		

			if i['destino'] == "Utilidades":
				if i['accion'] == 'actualizar':
					# ~ El registro existe y se actualiza
					CstsAdnlsM.objects.filter(id=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = CstsAdnlsM(idcstanls=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
					CstsAdnlsM.objects.filter(id=i["id"]).delete()
			
			if i['destino'] == "TOTALIZAR":
				ProductosM.objects.filter(id=idprod).update(costo=float(i["datos"]))
	
		return redirect(url)
		
	if request.method == 'GET':
		for i in ProductosDetallesM.objects.filter(idprd=idprod):
			# ~ print(i.idprd,"  ",i.idpart)
			if PartidasM.objects.filter(id = i.idpart).exists() == True:
				part = PartidasM.objects.get(id = i.idpart)			
				# ~ print(i.idpart)
				idatos.append(	
					{'id'      : i.id,
					 'idpart'  : i.idpart,  
					 'nombre'  : part.nomb,
					 'umedida' : part.unid,
					 'cumedida': part.cost,
					 'cantidad': i.cant,
					 'costo'   : round(i.cant*part.cost,2)
					})
				total = total + i.cant*part.cost
		totales["prddetlls"] = round(total,2)
		totprd = totprd + total
		total = 0.0
		
		for i in MaquiyHerraM.objects.filter(idprd=idprod):
			if InsumosM.objects.filter(id = i.idism).exists() == True:
				ism = InsumosM.objects.get(id = i.idism) #se debe filtrar con el idsim y que sea tipo MATERIAL
				mdatos.append(	
					{'id':       ism.id,  
					 'nombre':   ism.descrip,
					 'umedida':  ism.umedida,
					 'cumedida': ism.cumedida,
					 'cantidad': i.cant,
					 'costo':    round(ism.cumedida()*i.cant,2)
				})
				total = total + ism.cumedida()*i.cant
		totales["maqyherr"] = round(total,2)
		totprd = totprd + total
		total = 0.0
					
		for i in CstsAdnlsM.objects.filter(idprd = idprod):

			# ~ if CostosDescripcionM.objects.filter(id = i.idcstanls).filter(referencia="UMED").exists() == True:
			if CostosDescripcionM.objects.filter( Q(id = i.idcstanls) & Q(referencia="UMED") ).exists() == True:
				cstsadnls = CostosDescripcionM.objects.filter( Q(id = i.idcstanls) & Q(referencia="UMED") )
				for  k in cstsadnls:
					sbtotal = k.cumedida*i.cant
					cdatos.append(	
						{'id':       i.id,  
						 'nombre':   k.nombre,
						 'umedida':  k.umedida,
						 'cumedida': k.cumedida,
						 'cantidad': i.cant,
						 'costo':    round(sbtotal,2),
						 'referencia':k.referencia	
					})
					total = total + round(sbtotal,2)
		totales["cstsadnls"] = round(total,2)
		totprd = totprd + total
		total = 0.0
		# ~ totales['totprd'] = round(totprd,2)
		
		for i in CstsAdnlsM.objects.filter(idprd = idprod):

			if CostosDescripcionM.objects.filter(id = i.idcstanls).exclude(referencia="UMED").exists() == True:
				cstsadnls = CostosDescripcionM.objects.filter(id = i.idcstanls).exclude(referencia="UMED")
				sbtotal = (i.cant*( totales['maqyherr'] + totales['prddetlls'] + totales['cstsadnls'] ) )/100
				
				for  k in cstsadnls:
					udatos.append(	
						{'id':       i.id,  
						 'nombre':   k.nombre,
						 'umedida':  k.umedida,
						 'cumedida': k.cumedida,
						 'cantidad': i.cant,
						 'costo':    round(sbtotal,2),
						 'referencia':k.referencia	
					})
					total = total + round(sbtotal,2)
		totales["utilidades"] = round(total,2)
		totprd = totprd + total
		total = 0.0
		totales['totprd'] = round(totprd,2)
		print (totales) 
	# ~ print(totales)
	contexto['producto'] = producto 
	contexto['idatos'] = idatos
	contexto['mdatos'] = mdatos
	contexto['cdatos'] = cdatos
	contexto['udatos'] = udatos
	contexto['insumos'] =    InsumosM.objects.all().filter(tipo="MAT")
	contexto['materiales'] = MaquiyHerraM.objects.all()
	contexto['partidas'] =   PartidasM.objects.all()
	contexto['cstsanls'] =   CostosDescripcionM.objects.filter(referencia="UMED")
	contexto['utilidades'] =   CostosDescripcionM.objects.exclude(referencia="UMED")
	contexto['totales'] = totales
	
	return render(request,'detallar_producto.html',contexto)
