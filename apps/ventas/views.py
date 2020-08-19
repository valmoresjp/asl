from django.shortcuts import render,redirect
from datetime import datetime
from django.db.models import Sum

from django.contrib.auth.decorators import login_required

from apps.ventas.models import VentasM, ResumenM
from apps.ventas.forms import VentasF
from apps.clientes.models import ClientesM
from apps.prod.models import ProductosM, PartidasPRDM, MaterialesM
from apps.partida.models import PartidaDetallesM
from apps.mate.models import InsumosM

def inicio(request):
	datos = []
	ventas = VentasM.objects.all()
	for i in VentasM.objects.all():
		producto = ProductosM.objects.get(id=i.idprod)
		cliente  = ClientesM.objects.get(id=i.idclie)
		datos.append( {
					'idventa'  : i.id,
					'idclie'   : cliente.id,
					'idprod'   : producto.id,
					'cliente'  : cliente.nombre,
					'nprod'    : producto.nomb,
					'telefono' : cliente.telefono,
					'cantidad' : i.cant, 
					'costo'    : i.costo,
					'direccion': i.direc,
					'fhacd'    : i.fhacd,
					'fhentr'    : i.fhentr,
					'centr'    : i.centr,
					})
	contexto = {
				'ventas': datos,
	           }
	return render(request, "inicio_ventas.html", contexto)

@login_required(login_url='/inicio/ingreso')
def agregar(request, idprod, cantidad):
	
	if request.method == 'POST':
		datos= {
			'idprod' : request.POST['idprod'],
			'idclie' : request.POST['idclie'], 
			'cant'   : request.POST['cant'],   
			'costo'  : request.POST['costo'], 
			'pers'   : request.POST['pers'],
			'insm'   : request.POST['insm'], 
			'mate'   : request.POST['mate'], 
			'serv'   : request.POST['serv'],
			'utlds'  : request.POST['utlds'], 
			'obsrv'  : request.POST['obsrv'],
			'direc'  : request.POST['direc'],
			'centr'  : request.POST['centr'],
			'fhentr' : datetime.strptime(request.POST['fhentr'], '%Y-%m-%dT%H:%M'),
			'estado'  : request.POST['estado'],
			}
		form  = VentasF(datos)
		if form.is_valid():
			form.save()
			## almacenar datos en la tabla ResumenM
			t = datetime.now()
			ayo  = t.year
			mes  =  t.month
			r = ResumenM.objects.filter(ayo = ayo).filter(mes = mes)
			if r:
				ResumenM.objects.filter(ayo = ayo).filter(mes = mes).update(
							ayo	= ayo,
							mes = mes,
							ncli=0,
							nped =  int(datos['cant']) + r[0].nped,
							tota = float(datos['costo'])+ r[0].tota,
							util = float(datos['utlds'])+ r[0].util,
							insm = float(datos['insm'])+ r[0].insm,
							mate = float(datos['mate']) + r[0].mate,
							pers = float(datos['pers'])+ r[0].pers,
							serv = float(datos['serv']) + r[0].serv )
							
			else:
				a = ResumenM(
							ayo=ayo,
							mes=mes,
							ncli=0,
							nped=int(datos['cant'])  ,
							tota=float(datos['costo']) ,
							util=float(datos['utlds']) ,
							insm=float(datos['insm'])  ,
							mate=float(datos['mate'])  ,
							pers=float(datos['pers'])  ,
							serv=float(datos['serv']) ,
						)
				a.save()
			
			## Resta los productos vendidos del inventario, Tabla InsumosM
			
			## se obtiene el id de la partida
			for i in PartidasPRDM.objects.filter(idprd = request.POST['idprod']):
				## se obtiene el id del insumo
				for  k in PartidaDetallesM.objects.filter(idpart = i.idpart):
					## se resta el insumo del inventario
					insm = InsumosM.objects.get(id = k.idism)
					inventario = insm.inven - float(request.POST['cant'])*i.cant*k.cant
					# ~ print(insm.inven, "  ",request.POST['cant'],"  ", i.cant, "  ",k.cant, "  ",inventario)
					InsumosM.objects.filter(id = k.idism).update(inven = inventario)
					
			for i in MaterialesM.objects.filter(idprd = idprod):
				insm = InsumosM.objects.get(id = i.idmate)
				inventario = insm.inven - float(request.POST['cant'])*i.cant
				# ~ print(insm.inven, "  ",request.POST['cant'],"  ", i.cant,"   ",inventario)
				InsumosM.objects.filter(id = i.idmate).update(inven = inventario)
			
		else:
			print("error en el formulario")
			return render(request,'errores.html',{'form': form})

		return redirect ('inicio_ventas')
		
	if request.method == 'GET':
		producto = ProductosM.objects.get(id=idprod)
		datos= {
			'idprod' : idprod,
			'idclie' : 0, 
			'cant'   : cantidad,   
			'costo'  : round(producto.costo*cantidad,2), 
			'pers'   : round(producto.pers*cantidad,2),
			'insm'   : round(producto.insm*cantidad,2), 
			'mate'   : round(producto.mate*cantidad,2), 
			'serv'   : round(producto.serv*cantidad,2),
			'utlds'  : round(producto.utlds*cantidad,2), 
			'obsrv'  : "",
			'direc'  : "",
			'centr'  : 0,
			'fhentr' : "",
			'estado' : "EN_PRO"
			}
	
		form = VentasF(datos)
		c=[(0,'Seleccione un Cliente..')]
		clientes = ClientesM.objects.all()
		for i in clientes:
			c.append((i.id,i.nombre))
		form.fields['idclie'].choices = tuple(c)
		form.fields['idclie'].initial = [0]
		
		contexto = {
			'form': form,
			'producto':producto,
			}

	return render(request, "agregar_ventas.html", contexto)
	
@login_required(login_url='/inicio/ingreso')
def resumen(request, ayo ):
	aa = []
	periodo =""
	mes = {'1':'ENERO','2':'FEBRERO' ,'3':'MARZO','4':'ABRIL',
	       '5':'MAYO','6':'JUNIO' ,'7':'JULIO','8':'AGOSTO',
	       '9':'SEPTIEMBRE','10':'OCTUBRE','11':'NOVIEMBRE','12':'DICIEMBRE'
			}
	anual = {'clientes':0.0, 'pedidos':0.0, 'total':0.0, 'utilidades':0.0, 'personal':0.0, 'materiales':0.0, 'servicios':0.0, 'insumos':0.0}
	mensual=[]
	if request.method == 'GET':
		if ayo == 0:
			periodo = "Hasta la Fecha"
			anual['clientes']   = ResumenM.objects.aggregate(Sum('ncli'))['ncli__sum']
			anual['pedidos']    = ResumenM.objects.aggregate(Sum('nped'))['nped__sum']
			anual['total']      = ResumenM.objects.aggregate(Sum('tota'))['tota__sum']
			anual['utilidades'] = ResumenM.objects.aggregate(Sum('util'))['util__sum']
			anual['insumos']    = ResumenM.objects.aggregate(Sum('insm'))['insm__sum']
			anual['materiales'] = ResumenM.objects.aggregate(Sum('mate'))['mate__sum']
			anual['personal']   = ResumenM.objects.aggregate(Sum('pers'))['pers__sum']
			anual['servicios']  = ResumenM.objects.aggregate(Sum('serv'))['serv__sum']
			
			### se calculan los valores mensuales
			for i in ResumenM.objects.order_by('mes').values('mes').distinct():
				mensual.append(
						{'mes' : mes[str(i['mes'])],
						 'ncli': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('ncli'))['ncli__sum'],
						 'nped': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('nped'))['nped__sum'],
						 'tota': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('tota'))['tota__sum'],
						 'util': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('util'))['util__sum'],
						 'insm': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('insm'))['insm__sum'],
						 'mate':  ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('mate'))['mate__sum'],
						 'pers': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('pers'))['pers__sum'],
						 'serv': ResumenM.objects.filter(mes=i['mes']).aggregate(Sum('serv'))['serv__sum'],
						})
		else:
			periodo = ayo
			anual['clientes']   = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('ncli'))['ncli__sum']
			anual['pedidos']    = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('nped'))['nped__sum']
			anual['total']      = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('tota'))['tota__sum']
			anual['utilidades'] = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('util'))['util__sum']
			anual['insumos']    = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('insm'))['insm__sum']
			anual['materiales'] = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('mate'))['mate__sum']
			anual['personal']   = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('pers'))['pers__sum']
			anual['servicios']  = ResumenM.objects.filter(ayo=ayo).aggregate(Sum('serv'))['serv__sum']
			
			### se calculan los valores mensuales
			for i in ResumenM.objects.filter(ayo=ayo).order_by('mes').values('mes').distinct():
				mensual.append(
						{'mes' : mes[str(i['mes'])],
						 'ncli':ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('ncli'))['ncli__sum'],
						 'nped': ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('nped'))['nped__sum'],
						 'tota':ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('tota'))['tota__sum'],
						 'util':ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('util'))['util__sum'],
						 'insm': ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('insm'))['insm__sum'],
						 'mate': ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('mate'))['mate__sum'],
						 'pers': ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('pers'))['pers__sum'],
						 'serv': ResumenM.objects.filter(ayo=ayo).filter(mes=i['mes']).aggregate(Sum('serv'))['serv__sum'],
						})			
		
		for i in  ResumenM.objects.values('ayo').order_by('-ayo').distinct():
			aa.append(i['ayo']) # lista de años
	contexto = {
		'periodo' : periodo,	
		'ayos'    : aa,
		'anual'   : anual,
		'mensual' : mensual,
	}
	return render(request,'resumen_ventas.html', contexto)	
