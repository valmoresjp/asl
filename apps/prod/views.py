from django.shortcuts import render, redirect
import json
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM, PartidaDetallesM
from apps.prod.models import ProductosM, ProductosDetallesM, MaquiyHerraM, CstsAdnlsM
from apps.conf.models import CostosDescripcionM
from apps.prod.forms import ProductosF

# Create your views here.

def inicio(request):

	# ~ registro = ProductosM.objects.values()
	obj = ProductosM.objects.all()
	contexto = {
				'obj': obj,
	            }
	
	return render (request,'inicio_producto.html', contexto)

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
		print("ingresando a nuevo_producto")
		form = ProductosF()
	return render(request,'nuevo_producto.html', {'form': form})

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
	
def eliminar(request, idprod):

	if request.method == 'POST':

		url_ant = "inicio_producto"
		reg = ProductosM.objects.get(id=idprod)
		print (" NOTA: se deben eliminar los registros de materiales pertenecientes a este producto")
		print ("       estos están ubicados en la tabla ProductosDetallesM")
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
	totales = { 'totprd':0.0, 'prddetlls':0.0, 'maqyherr': 0.0, 'cstsadnls': 0.0 }
	totprd = 0.0
	total = 0.0

	producto   = ProductosM.objects.get(id=idprod)
	# ~ materiales = MaquiyHerraM.objects.all()
	partida    = PartidaDetallesM.objects.all()
	# ~ prd_deta   = ProductosDetallesM.objects.filter(idprd=idprod)

	if request.method =='POST':
		print("DETALLAR: metodo POST")
		url = "/productos/detallar/" + str(idprod) + "/"
		print(url)
		print(request.POST['ObjDatos'])
		for i in json.loads(request.POST["ObjDatos"]):
			print(i['accion'], "  ",i['destino'])
			if i['destino'] == "INSUMOS":
				print("INSUMOS")
				if i['accion'] == 'actualizar':
					res = ProductosDetallesM.objects.filter(idprd=idprod).filter(idpart=i["id"]).exists()
					if res == True :
						# ~ El registro existe y se actualiza
						ProductosDetallesM.objects.filter(idpart=i["id"]).update(cant=i["datos"])
					else:
						# ~ El registro no existe, se crea un nuevo registro
						g = ProductosDetallesM(idpart=i["id"], idprd=idprod, cant=i["datos"])
						g.save()
					
				if i['accion'] == 'eliminar':
					ProductosDetallesM.objects.filter(id=i["id"]).delete()
					
			if i['destino'] == "MAQYHERR":
				if i['accion'] == 'actualizar':
					res = MaquiyHerraM.objects.filter(idprd=idprod).filter(idism=i["id"]).exists()
					if res==True :
						# ~ El registro existe y se actualiza
						MaquiyHerraM.objects.filter(idism=i["id"]).update(cant=i["datos"])
					else:
						# ~ El registro no existe, se crea un nuevo registro
						g = MaquiyHerraM(idism=i["id"], idprd=idprod, cant=i["datos"])
						g.save()
					
				if i['accion'] == 'eliminar':
						MaquiyHerraM.objects.filter(id=i["id"]).delete()				
				
			if i['destino'] == "CSTSADNLS":
				if i['accion'] == 'actualizar':
					res = CstsAdnlsM.objects.filter(idprd=idprod).filter(idcstanls=i["id"]).exists()
					if res==True :
						# ~ El registro existe y se actualiza
						CstsAdnlsM.objects.filter(idcstanls=i["id"]).update(cant=i["datos"])
					else:
						# ~ El registro no existe, se crea un nuevo registro
						g = CstsAdnlsM(idcstanls=i["id"], idprd=idprod, cant=i["datos"])
						g.save()
					
				if i['accion'] == 'eliminar':
						CstsAdnlsM.objects.filter(id=i["id"]).delete()		
		
		return redirect(url)
		
	if request.method == 'GET':
		for i in ProductosDetallesM.objects.filter(idprd=idprod):
			part = PartidasM.objects.get(id = i.idpart)
			idatos.append(	
				{'id':       i.id,  
				 'nombre':   part.nomb,
				 'umedida':  i.unid,
				 'cumedida': part.cost,
				 'cantidad': i.cant,
				 'costo':    i.cant*part.cost
				})
			total = total + i.cant*part.cost
		totales["prddetlls"] = total
		totprd = totprd + total
		total = 0.0
		
		for i in MaquiyHerraM.objects.all():
			ism = InsumosM.objects.get(id = i.idism) #se debe filtrar con el idsim y que sea tipo MATERIAL
			mdatos.append(	
				{'id':       i.id,  
				 'nombre':   ism.descrip,
				 'umedida':  ism.umedida,
				 'cumedida': ism.cumedida,
				 'cantidad': i.cant,
				 'costo':    ism.cumedida()*i.cant
			})
			total = total + ism.cumedida()*i.cant
		totales["maqyherr"] = total
		totprd = totprd + total
		total = 0.0
					
		for i in CstsAdnlsM.objects.filter(idprd = idprod):
			print(i.idcstanls)
			cstsadnls = CostosDescripcionM.objects.get(id = i.idcstanls) 
			cdatos.append(	
				{'id':       i.id,  
				 'nombre':   cstsadnls.nombre,
				 'umedida':  cstsadnls.umedida,
				 'cumedida': cstsadnls.cumedida,
				 'cantidad': i.cant,
				 'costo':    cstsadnls.cumedida*i.cant
			})
			total = total + cstsadnls.cumedida*i.cant
		
		totales["cstsadnls"] = total
		totprd = totprd + total
		totales['totprd'] = round(totprd,2)
		total = 0.0
		
	print(totales)
	contexto['producto'] = producto 
	contexto['idatos'] = idatos
	contexto['mdatos'] = mdatos
	contexto['cdatos'] = cdatos
	contexto['insumos'] =    InsumosM.objects.all().filter(tipo="MAT")
	contexto['materiales'] = MaquiyHerraM.objects.all()
	contexto['partidas'] =   PartidasM.objects.all()
	contexto['cstsanls'] =   CostosDescripcionM.objects.all()
	contexto['totales'] = totales
	
	return render(request,'detallar_producto.html',contexto)
