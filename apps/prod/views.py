from django.shortcuts import render, redirect
import json
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM, PartidaDetallesM
from apps.prod.models import ProductosM, PartidasPRDM, MaterialesM, ServiciosM, PersonalM#, MaquiyHerraM, CstsAdnlsM,
from apps.prod.forms import ProductosF#, VentasF
from apps.conf.models import CostosDescripcionM, UtilidadesDetallesM, UtilidadesM
from apps.clientes.models import ClientesM
from django.db.models import Q

from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):

	obj = ProductosM.objects.all()
	contexto = {
				'obj': obj,
	            }

	return render (request,'inicio_producto-1.html', contexto)

@login_required(login_url='/inicio/ingreso')
def nuevo(request):
	print(request.POST)
	if request.method == 'POST':
		form = ProductosF(request.POST)
		if form.is_valid():
			form.save()
		else:
			return render(request,'errores.html',{'form': form})

		return redirect ('inicio_producto')
	else:
		form = ProductosF()
	return render(request,'nuevo_producto.html', {'form': form})

@login_required(login_url='/inicio/ingreso')
def editar(request, idprod ):
	producto = ProductosM.objects.get(id=idprod)
	print(request.POST)
	if request.method == 'GET':
		form = ProductosF(instance=producto)
	else:
		form = ProductosF(request.POST, instance=producto)
		if form.is_valid():
			form.save()
		else:
			return render(request,'errores.html',{'form': form})
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

	contexto = {}
	pdatos  = []
	mdatos  = []
	sdatos  = []
	pedatos = []
	udatos  = []

	totales = { 'totprd':0.0, 'partidas':0.0, 'materiales': 0.0, 'servicios': 0.0, 'personal': 0.0 }
	totprd = 0.0
	total = 0.0

	producto   = ProductosM.objects.get(id=idprod)

	if request.method =='POST':
		url = "/productos/detallar/" + str(idprod) + "/"
		for i in json.loads(request.POST["ObjDatos"]):

			if i['destino'] == "Insumos":
				if i['accion'] == 'actualizar':
					PartidasPRDM.objects.filter(idprd=idprod).filter(idpart=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					g = PartidasPRDM(idpart=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
#<<<<<<< HEAD
#					ProductosDetallesM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()
#
#=======
					PartidasPRDM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()

#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
			if i['destino'] == "Materiales":
				if i['accion'] == 'actualizar':
					# ~ El registro existe y se actualiza
					a = MaterialesM.objects.filter(idprd=idprod).filter(idmate=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
#<<<<<<< HEAD
#					g = MaquiyHerraM(idism=i["id"], idprd=idprod, cant=i["datos"])#
#					g.save()
#				if i['accion'] == 'eliminar':
#					MaquiyHerraM.objects.filter(idprd=idprod).filter(idism=i["id"]).delete()
#
#			if i['destino'] == "CostosAdicionales":
#=======
					g = MaterialesM(idmate=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
					MaterialesM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()

			if i['destino'] == "Servicios":
#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
				if i['accion'] == 'actualizar':
					# ~ El registro existe yf se actualiza
					ServiciosM.objects.filter(idprd=idprod).filter(idserv=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = ServiciosM(idserv=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
#<<<<<<< HEAD
#					CstsAdnlsM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()
#
#			if i['destino'] == "Utilidades":
#=======
					ServiciosM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()

			if i['destino'] == "Personal":
#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
				if i['accion'] == 'actualizar':
					# ~ El registro existe y se actualiza
					PersonalM.objects.filter(idprd=idprod).filter(idpers=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = PersonalM(idpers=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
#<<<<<<< HEAD
#<<<<<<< HEAD
#					CstsAdnlsM.objects.filter(id=i["id"]).delete()
#
#			if i['destino'] == "TOTALIZAR":
#				ProductosM.objects.filter(id=idprod).update(costo=float(i["datos"]))
#
#=======
					PersonalM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()

			# ~ if i['destino'] == "Utilidades":
				# ~ print(i['destino'], ", Utilidades   ")
				# ~ if i['accion'] == 'actualizar':
					# ~ ## ~ El registro existe y se actualiza
					# ~ CstsAdnlsM.objects.filter(id=i["id"]).update(cant=i["datos"])
				# ~ if i['accion'] == 'nuevo':
					# ~ ## ~ El registro no existe, se crea un nuevo registro
					# ~ g = CstsAdnlsM(idcstanls=i["id"], idprd=idprod, cant=i["datos"])
					# ~ g.save()
				# ~ if i['accion'] == 'eliminar':
					# ~ CstsAdnlsM.objects.filter(id=i["id"]).delete()

#=======
					PersonalM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()

#>>>>>>> 6be65c8e5726b6be39b21e937e8909216ecd90fd
			if i['destino'] == "TOTALIZAR":
				ProductosM.objects.filter(id=idprod).update(
				insm   = float( i["datos"]['insm']),
				mate   = float( i["datos"]['mate']),
				pers   = float( i["datos"]['pers']),
				serv   = float( i["datos"]['serv']),
				pinsm  = float( i["datos"]['pinsm']), #porcentaje de utilidad con respecto a los insumos
				pmate  = float( i["datos"]['pmate']), # porcentaje de utilidad con respecto a los   materiales
				ppers  = float( i["datos"]['ppers']), #porcentaje de utilidad con respecto al personal
				pserv  = float( i["datos"]['pserv']), #porcentaje de utilidad con respecto a los  servicios
				utlds  = float( i["datos"]['utlds']),
				costo  = float( i["datos"]['costo']))

#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
		return redirect(url)


	if request.method == 'GET':
		for i in PartidasPRDM.objects.filter(idprd=idprod):
			if PartidasM.objects.filter(id = i.idpart).exists() == True:
#<<<<<<< HEAD
#				part = PartidasM.objects.get(id = i.idpart)
#				idatos.append(
#=======
				part = PartidasM.objects.get(id = i.idpart)
				pdatos.append(
#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
					{'id'      : i.id,
					 'idpart'  : i.idpart,
					 'nombre'  : part.nomb,
					 'umedida' : part.unid,
					 'cumedida': part.cost,
					 'cantidad': i.cant,
					 'costo'   : round(i.cant*part.cost,2)
					})
				total = total + i.cant*part.cost
		totales["partidas"] = round(total,2)
		totprd = totprd + total
		total = 0.0
#<<<<<<< HEAD
#
#		for i in MaquiyHerraM.objects.filter(idprd=idprod):
#			if InsumosM.objects.filter(id = i.idism).exists() == True:
#				ism = InsumosM.objects.get(id = i.idism)
#				mdatos.append(
#					{'id':       ism.id,
#					 'nombre':   ism.descrip,
#					 'umedida':  ism.umedida,
#					 'cumedida': ism.cumedida,
#=======

		for i in MaterialesM.objects.filter(idprd=idprod):
			if InsumosM.objects.filter(tipo="MAT").filter(id = i.idmate).exists() == True:
				mate = InsumosM.objects.get(id = i.idmate)
				mdatos.append(
					{'id':       i.id,
					 'idmate':   mate.id,
					 'nombre':   mate.descrip,
					 'umedida':  mate.umedida,
					 'cumedida': mate.cumedida,
#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
					 'cantidad': i.cant,
					 'costo':    round(mate.cumedida()*i.cant,2)
				})
				total = total + mate.cumedida()*i.cant
		totales["materiales"] = round(total,2)
		totprd = totprd + total
		total = 0.0
#<<<<<<< HEAD
#
#		for i in CstsAdnlsM.objects.filter(idprd = idprod):
#
##				cstsadnls = CostosDescripcionM.objects.filter( Q(id = i.idcstanls) & Q(referencia="UMED") )
#				for  k in cstsadnls:
#					sbtotal = k.cumedida*i.cant
#					cdatos.append(
#						{'id':       i.id,
#						 'nombre':   k.nombre,
##						 'umedida':  k.umedida,
#						 'cumedida': k.cumedida,
#						 'cantidad': i.cant,
#						 'costo':    round(sbtotal,2),
#						 'referencia':k.referencia
#					})
#					total = total + round(sbtotal,2)
#		totales["cstsadnls"] = round(total,2)
#		totprd = totprd + total
#		total = 0.0
#
#		for i in CstsAdnlsM.objects.filter(idprd = idprod):
#
#			if CostosDescripcionM.objects.filter(id = i.idcstanls).exclude(referencia="UMED").exists() == True:
#				cstsadnls = CostosDescripcionM.objects.filter(id = i.idcstanls).exclude(referencia="UMED")
#				sbtotal = (i.cant*( totales['maqyherr'] + totales['prddetlls'] + totales['cstsadnls'] ) )/100
#
#				for  k in cstsadnls:
#					udatos.append(
#						{'id':       i.id,
#						 'nombre':   k.nombre,
#						 'umedida':  k.umedida,
#						 'cumedida': k.cumedida,
#						 'cantidad': i.cant,
#						 'costo':    round(sbtotal,2),
#						 'referencia':k.referencia
#=======

		for i in ServiciosM.objects.filter(idprd = idprod):
			if InsumosM.objects.filter(tipo="SER").filter(id = i.idserv).exists() == True:
				serv = InsumosM.objects.get(id = i.idserv)
				sdatos.append(
					{'id'      : i.id,
					 'idser'   : serv.id,
					'nombre'   : serv.descrip,
					'umedida'  : serv.umedida,
					'cumedida' : serv.cumedida,
					'cantidad' : i.cant,
					'costo'    : round(serv.cumedida()*i.cant,2)
				})
			total = total + serv.cumedida()*i.cant
		totales["servicios"] = round(total,2)
		totprd = totprd + total
		total = 0.0

		for i in PersonalM.objects.filter(idprd = idprod):
			if InsumosM.objects.filter(tipo="PER").filter(id = i.idpers).exists() == True:
				pers = InsumosM.objects.get(id = i.idpers)
				pedatos.append(
					{'id'       : i.id,
					 'nombre'   : pers.descrip,
					 'umedida'  : pers.umedida,
					 'cumedida' : pers.cumedida,
					 'cantidad' : i.cant,
					 'costo'    : round(pers.cumedida()*i.cant,2)
#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
					})
				total = total + pers.cumedida()*i.cant
		totales["personal"] = round(total,2)
		totprd = totprd + total
		total = 0.0
		totales['totprd'] = round(totprd,2)
#<<<<<<< HEAD

#	contexto['producto'] = producto
#	contexto['idatos'] = idatos
#	contexto['mdatos'] = mdatos
#	contexto['cdatos'] = cdatos
#	contexto['udatos'] = udatos
#	contexto['insumos'] =    InsumosM.objects.all().filter(tipo="MAT")
#	contexto['materiales'] = MaquiyHerraM.objects.all()
#	contexto['partidas'] =   PartidasM.objects.all()
#	contexto['cstsanls'] =   CostosDescripcionM.objects.filter(referencia="UMED")
#	contexto['utilidades'] =   CostosDescripcionM.objects.exclude(referencia="UMED")
#	contexto['totales'] = totales
#
#	return render(request,'detallar_producto.html',contexto)
#=======

		for i in UtilidadesDetallesM.objects.filter(idprod = idprod):

			util = UtilidadesM.objects.filter(id = i.idutil)
			for  k in util:
				udatos.append(
						{'id':     i.id,
						 'item':   k.descripcion,
						 'porcentaje':  i.porcentaje,
						 'valor': i.valor,
					})

	contexto['producto']   = producto
	contexto['pdatos']     = pdatos
	contexto['partidas']   = PartidasM.objects.all()
	contexto['mdatos']     = mdatos
	contexto['materiales'] = InsumosM.objects.all().filter(tipo="MAT")
	contexto['sdatos']     = sdatos
	contexto['servicios']  = InsumosM.objects.all().filter(tipo="SER")
	contexto['pedatos']    = pedatos
	contexto['personal']   = InsumosM.objects.all().filter(tipo="PER")
	contexto['udatos']     = udatos
	contexto['totales'] = totales

	return render(request,'detallar_producto-v2.html',contexto)

#>>>>>>> 42be4006e837b24623d8c40a831b0470ab55a6f0
