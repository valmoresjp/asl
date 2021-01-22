from django.shortcuts import render,redirect
from datetime import datetime, date, time, timedelta
import time
from django.db.models import Sum
from django.utils import timezone
import pytz

from django.contrib.auth.decorators import login_required

from apps.ventas.models import VentasM, ResumenM
from apps.ventas.forms import VentasF
from apps.clientes.models import ClientesM
from apps.prod.models import ProductosM, PartidasPRDM, MaterialesM
from apps.partida.models import PartidaDetallesM
from apps.mate.models import InsumosM, FacturasM

# ~ from plotly.offline import plot
# ~ from plotly.graph_objs import Scatter

porcentaje = lambda valor, referencia: (valor*100)/(1 if referencia==0 else referencia)
retornar_num = lambda valor: valor or 0

def variacion_dif(valor, referencia):
	# ~ sube  = {'icono':"fa fa-1x fa-arrow-circle-up", "estilo":"color:green;"}
	# ~ baja  = {'icono':"fa fa-1x fa-arrow-circle-down", "estilo":"color:red;"}
	# ~ igual = {'icono':"fa fa-1x fa-arrow-circle-down", "estilo":"color:yellow;"} #futuro
	resultado = {}
	resultado['valor'] = valor
	if referencia == 0:
		resultado['var'] = 100
	else:
		resultado['var'] = ((valor-referencia)*100)/referencia
	if resultado['var'] >= 0:
		# ~ if resultado['var'] > 999.9:
			# ~ resultado['var'] = "> 999.9"
		resultado['estilo'] = {'icono':"fa fa-1x fa-arrow-circle-up", "estilo":"color:green;"}
	else:
		resultado['var'] = abs(resultado['var'])
		resultado['estilo'] =  {'icono':"fa fa-1x fa-arrow-circle-down", "estilo":"color:red;"}				
	return (resultado)

def inicio(request):
	datos = []
	ventas = VentasM.objects.order_by('-fhacd', 'fhentr') #all().
	
	for i in ventas:
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
					'fhentr'   : i.fhentr,
					'centr'    : i.centr,
					})
	# ~ print(datetime.datetime.now().year)
	contexto = {
				'ventas': datos,
				'ayo': datetime.now().year
	           }
	return render(request, "inicio_ventas.html", contexto)

@login_required(login_url='/inicio/ingreso')
def agregar(request, idprod, cantidad):
	
	if request.method == 'POST':
		
		# se convierte el tiempo en UTC para ser almacenado en la BD
		local = pytz.timezone ("America/Santiago") 
		naive = datetime.strptime (request.POST['fhentr'], "%d-%m-%Y %H:%M") 
		local_dt = local.localize(naive, is_dst=None) 
		utc_dt = local_dt.astimezone (pytz.utc)
		fecha_utc = utc_dt.strftime ("%d-%m-%Y %H:%M")
		
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
			'fhentr' : fecha_utc,
			'estado' : request.POST['estado'],
			}

		form  = VentasF(datos)
		if int(datos['idclie']) == 0:
			form.add_error('idclie','Seleccione un cliente')
		
		if datos['cant'].isnumeric():
			if int(datos['cant']) < 0:
				form.add_error('cant','La cantidad debe ser mayor que 1')
		else:
			form.add_error('cant','La cantidad debe ser mayor que 1')


		if form.is_valid():# and existe:
			form.save()
			## almacenar datos en la tabla ResumenM
			t = datetime.now() # tiempo en UTC
			ayo  = t.year
			mes  =  t.month
			if ResumenM.objects.filter(ayo = ayo,mes = mes).exists():
				r = ResumenM.objects.filter(ayo = ayo,mes = mes)
				
				ResumenM.objects.filter(ayo = ayo,mes = mes).update(
							ayo	= ayo,
							mes = mes,
							ncli_t = ClientesM.objects.filter(fhreg__year=ayo).count(), #no es necesario
							ncli_n = ClientesM.objects.filter(fhreg__year=ayo, fhreg__month=mes).count(),#no es necesario
							ncli_a = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).order_by('idclie').values('idclie').distinct().count(),#VentasM.objects.filter(estado__gte=1).filter(estado__lte=3).count(),
							npeds  = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).filter(estado__gte=0, estado__lte=99).count(),# int(datos['cant']) + r[0].npedv,
							npedv  = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).filter(estado__gte=1, estado__lte=3).count(),# int(datos['cant']) + r[0].npedv,
							npedc  = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).filter(estado=99).count(),#int(datos['cant']) + r[0].nped,
							nprdv  = -1,#int(datos['cant']) + r[0].nped,
							)
							# ~ tota = float(datos['costo'])+ r[0].tota,
							# ~ util = float(datos['utlds'])+ r[0].util,
							# ~ insm = float(datos['insm'])+ r[0].insm,
							# ~ mate = float(datos['mate']) + r[0].mate,
							# ~ pers = float(datos['pers'])+ r[0].pers,
							# ~ serv = float(datos['serv']) + r[0].serv )
							
			else:
				a = ResumenM(
							ayo=ayo,
							mes=mes,
							ncli_t = ClientesM.objects.filter(fhreg__year=ayo).count(),
							ncli_n = ClientesM.objects.filter(fhreg__year=ayo, fhreg__month=mes).count(),
							ncli_a = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).order_by('idclie').values('idclie').distinct().count(),
							npeds  = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).filter(estado__gte=0, estado__lte=3).count(),# int(datos['cant']) + r[0].npedv,
							npedv  = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).filter(estado__gte=1, estado__lte=3).count(),# int(datos['cant']) + r[0].npedv,
							npedc  = VentasM.objects.filter(fhacd__year=ayo, fhacd__month=mes).filter(estado=99).count(),#int(datos['cant']) + r[0].nped,
							nprdv  = -1,#int(datos['cant']) + r[0].nped,
							tota=0.0,#float(datos['costo']) ,
							util=0.0,#float(datos['utlds']) ,
							insm=0.0,#float(datos['insm'])  ,
							mate=0.0,#float(datos['mate'])  ,
							pers=0.0,#float(datos['pers'])  ,
							serv=0.0,#float(datos['serv']) ,
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
			
			for  i in list(form.errors.keys()):
				print("error:", i)
				form.fields[i].widget.attrs.update({'class': 'form-control borde_error'})
			
			producto = ProductosM.objects.get(id=idprod)
			form.fields['fhentr'].initial = request.POST['fhentr']
			contexto = {
						'form': form,
						'producto':producto,
						}	
			# ~ verifico con form.errors los campos que tienen fallas
			# ~ y los marco con el borde rojo, luego redirecciono la pagina 
			# ~ al formulario  a con los nuevos atributos( con los campos marcados)
			 # ~ ("agregar_ventas.html", contexto)
			return render(request, "agregar_ventas.html", contexto)
			# ~ return render(request,'errores.html',{'form': form})

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
			'fhentr' : time.strftime("%d-%m-%Y 10:00",time.gmtime(time.time()+3600*24*3)),
			'estado' : "EN_PRO"
			}
	
		form = VentasF(initial=datos)
		c=[(0,'Seleccione un Cliente..')]
		clientes = ClientesM.objects.all()
		for i in clientes:
			c.append((i.id,i.nombre))
		form.fields['idclie'].choices = tuple(c)
		form.fields['idclie'].initial = [0]
		# ~ form.fields['idclie'].widget.attrs.update({'class': 'form-control borde_error'})

		contexto = {
			'form': form,
			'producto':producto,
			}

	return render(request, "agregar_ventas.html", contexto)
	
@login_required(login_url='/inicio/ingreso')
def resumen(request, ayo ):
	aa = []
	periodo =""
	mes = {1:'ENERO',2:'FEBRERO' ,3:'MARZO',4:'ABRIL',
	       5:'MAYO',6:'JUNIO' ,7:'JULIO',8:'AGOSTO',
	       9:'SEPTIEMBRE',10:'OCTUBRE',11:'NOVIEMBRE',12:'DICIEMBRE'
		}
	sube = {'icono':"fa fa-1x fa-arrow-circle-up", "estilo":"color:green;"}
	baja = {'icono':"fa fa-1x fa-arrow-circle-down", "estilo":"color:red;"}
	mensual=[]
	datos_mensuales = []
	if request.method == 'GET':
		print("INGRESO A RESUMEN DE VENTAS")
		
		# se verifica si existe registro alguno cuando cambia de año, en caso contrario crea un registro 
		# para comparar con el ayo anterio y mes anterior. Este registro tendra sus valores minimos, es decir 0.0
		
		if ResumenM.objects.filter(ayo=ayo).order_by('mes').values('mes').distinct().count() <= 0:
			#se crea el registro
			tmp = ResumenM(ayo=ayo, mes=1)
			tmp.save()

		
		for i in ResumenM.objects.filter(ayo=ayo).order_by('mes').values('mes').distinct():
			print("reg: ", i) 
			mes_ayo_act={'ayo':ayo,'mes':i['mes']} #año actual y mes actual
			
			#se determina el mes anterior.
			if mes_ayo_act['mes'] == 1:
				mes_ant = {'ayo':mes_ayo_act['ayo']-1,'mes':12} 
			else:
				mes_ant = {'ayo':mes_ayo_act['ayo'],'mes':mes_ayo_act['mes']-1}
			 
			mes_ayo_ant={'ayo':mes_ayo_act['ayo']-1,'mes':mes_ayo_act['mes']} #Mismo mes pero del año anterior
			
			
			print(mes_ayo_ant)
			print(mes_ant)
			print(mes_ayo_act)
			
			 #se verifica si el año y el mes existen en los registro,
			 # en caso de no existir se crea el registro con valores 
			 #nulos, es decir, ceros.Esto ayuda a evitar errores cuando 
			 # no se realiza ninguna venta durante el mes.
			 # ~ datos_mes_ayo_ant = [{'ayo': 2020, 'mes': mes_ant['mes'], 'ncli_t': 0, 'ncli_n': 0, 'ncli_a': 0, 'npedv':0, 'npedc': 0, 'nprdv': 0, 'tota': 0, 'util': 0, 'insm':0, 'mate': 0.0, 'pers': 0.0, 'serv': 0.0}]
			if ResumenM.objects.filter(ayo=mes_ant['ayo']).exists():
				if ResumenM.objects.filter(ayo=mes_ant['ayo'],mes=mes_ant['mes']).exists():
					tmp_mes_ant = ResumenM.objects.filter(ayo=mes_ant['ayo'],mes=mes_ant['mes']).values() #datos del mes anterior del año anterior 
				else:
					tmp_mes_ant = [{'ayo': mes_ant['ayo'], 'mes': mes_ant['mes'], 'ncli_t': 0, 'ncli_n': 0, 'ncli_a': 0, 'npeds':0,'npedv':0, 'npedc': 0, 'nprdv': 0, 'tota': 0, 'util': 0, 'insm':0, 'mate': 0.0, 'pers': 0.0, 'serv': 0.0}]
			else:
				tmp_mes_ant = [{'ayo': mes_ant['ayo'], 'mes': mes_ant['mes'], 'ncli_t': 0, 'ncli_n': 0, 'ncli_a': 0, 'npeds':0,'npedv':0, 'npedc': 0, 'nprdv': 0, 'tota': 0, 'util': 0, 'insm':0, 'mate': 0.0, 'pers': 0.0, 'serv': 0.0}]

			if ResumenM.objects.filter(ayo=mes_ayo_ant['ayo']).exists():
				if ResumenM.objects.filter(ayo=mes_ayo_ant['ayo'],mes=mes_ayo_ant['mes']).exists():
					tmp_mes_ayo_ant = ResumenM.objects.filter(ayo=mes_ayo_ant['ayo'],mes=mes_ayo_ant['mes']).values() #datos del mes anterior del año anterior 
				else:
					tmp_mes_ayo_ant = [{'ayo': mes_ayo_ant['ayo'], 'mes': mes_ayo_ant['mes'], 'ncli_t': 0, 'ncli_n': 0, 'ncli_a': 0, 'npeds':0,'npedv':0, 'npedc': 0, 'nprdv': 0, 'tota': 0, 'util': 0, 'insm':0, 'mate': 0.0, 'pers': 0.0, 'serv': 0.0}]
			else:
				tmp_mes_ayo_ant = [{'ayo': mes_ayo_ant['ayo'], 'mes': mes_ayo_ant['mes'], 'ncli_t': 0, 'ncli_n': 0, 'ncli_a': 0, 'npeds':0,'npedv':0, 'npedc': 0, 'nprdv': 0, 'tota': 0, 'util': 0, 'insm':0, 'mate': 0.0, 'pers': 0.0, 'serv': 0.0}]

			datos_mes_act_ayo_act = ResumenM.objects.filter(ayo=mes_ayo_act['ayo'],mes=mes_ayo_act['mes']).values() #datos del mes actual del año actual
			datos_mes_ant_ayo_act = tmp_mes_ant
			datos_mes_ayo_ant     = tmp_mes_ayo_ant #datos del mes actual del año anterior
		
			#variacion de clientes con respecto al mes anterior
			clientes_mes = variacion_dif(datos_mes_act_ayo_act[0]['ncli_n'],datos_mes_ant_ayo_act[0]['ncli_n'])

			#variacion de clientes con respecto al mismo mes del año anterior
			clientes_ayo_ant_acum = ClientesM.objects.filter(fhreg__year = mes_ayo_ant['ayo']).count()
			clientes_anual = variacion_dif(datos_mes_act_ayo_act[0]['ncli_t'],clientes_ayo_ant_acum)

			gasto_mes = variacion_dif(datos_mes_act_ayo_act[0]['tota'],  datos_mes_ant_ayo_act[0]['tota'])
			
			# ~ CALUCLOS PARA DATOS REFERENTES A LOS PEDIDOS
			datos_pedidos_ayo_act = datos_mes_act_ayo_act#ResumenM.objects.filter(ayo=mes_ayo_act['ayo'],mes=mes_ayo_act['mes']).values()
			pedidos_solicitados_mes = datos_mes_act_ayo_act[0]
			
			#variacion mensual de los pedidos solicitados
			ped_soli_mes = variacion_dif (datos_mes_act_ayo_act[0]['npeds'],datos_mes_ant_ayo_act[0]['npeds'])
			
			#variacion mensual de los pedidos vendidos
			ped_vend_mes = variacion_dif(datos_mes_act_ayo_act[0]['npedv'],datos_mes_ant_ayo_act[0]['npedv'])

			#variacion mensual de los pedidos cancelados
			ped_canc_mes = variacion_dif(datos_mes_act_ayo_act[0]['npedc'],datos_mes_ant_ayo_act[0]['npedc'])
			
			#representacion en porcentaje del total de pedidos solicitados
			ped_proc_mes_act =  retornar_num(VentasM.objects.filter(fhacd__year=mes_ayo_act['ayo'], fhacd__month=mes_ayo_act['mes']).filter(estado=0).count())
			ped_proc_mes_ant =  retornar_num(VentasM.objects.filter(fhacd__year=mes_ayo_act['ayo'], fhacd__month=mes_ant['mes']).filter(estado=0).count())
			
			ped_proc_mes = variacion_dif (ped_proc_mes_act, ped_proc_mes_ant)
			
			#variacion ANUAL de los pedidos vendidos
			ped_acum_ayo_act = retornar_num(ResumenM.objects.filter(ayo=mes_ayo_act['ayo'], mes__lte=mes_ayo_act['mes']).aggregate(Sum('npedv'))['npedv__sum'])
			ped_acum_ayo_ant = retornar_num(ResumenM.objects.filter(ayo=mes_ayo_ant['ayo']).aggregate(Sum('npedv'))['npedv__sum'])
			ped_vend_anual = variacion_dif ( ped_acum_ayo_act, ped_acum_ayo_ant)


            # ~ CALCULOS REFENTES A LAS VENTAS
			venta_por_aprobar = {}
			venta_cancelada   = {}
			venta_efectiva    = {}
			venta_proyectada                = retornar_num(VentasM.objects.filter(fhacd__year=mes_ayo_act['ayo'], fhacd__month=mes_ayo_act['mes']).aggregate(Sum('costo'))['costo__sum'])
			venta_por_aprobar['valor']      = retornar_num(VentasM.objects.filter(fhacd__year=mes_ayo_act['ayo'], fhacd__month=mes_ayo_act['mes']).filter(estado=0).aggregate(Sum('costo'))['costo__sum'])
			venta_por_aprobar['porcentaje'] = porcentaje (venta_por_aprobar['valor'],venta_proyectada)
			venta_cancelada['valor']        = retornar_num(VentasM.objects.filter(fhacd__year=mes_ayo_act['ayo'], fhacd__month=mes_ayo_act['mes']).filter(estado=99).aggregate(Sum('costo'))['costo__sum'])
			venta_cancelada['porcentaje']   = porcentaje(venta_cancelada['valor'], venta_proyectada)
			venta_efectiva['valor']         = retornar_num(VentasM.objects.filter(fhacd__year=mes_ayo_act['ayo'], fhacd__month=mes_ayo_act['mes']).filter(estado__gte=1,estado__lte=3).aggregate(Sum('costo'))['costo__sum'])
			venta_efectiva['porcentaje']    = porcentaje(venta_efectiva['valor'], venta_proyectada)
			
			 
			 
			# ~ CALCULOS PARA DATOS REFERENTES AL PERSONAL
			
			#variacion actual con respecto al mes anterior del mismo año
			produccion_per_mes_act_ayo_act = variacion_dif(datos_mes_act_ayo_act[0]['pers'], datos_mes_ant_ayo_act[0]['pers'])
			
			#variacion actual con respecto al año anterior
			produccion_per_ayo_act  = ResumenM.objects.filter(ayo=mes_ayo_act['ayo'], mes__lte=mes_ayo_act['mes']).aggregate(Sum('pers'))['pers__sum']
			produccion_per_ayo_ant  = retornar_num(ResumenM.objects.filter(ayo=mes_ayo_ant['ayo']).aggregate(Sum('pers'))['pers__sum'])
			produccion_per_ayo_act  = variacion_dif(produccion_per_ayo_act, retornar_num(produccion_per_ayo_ant))
			num_personal            = InsumosM.objects.filter(tipo="PER").count()
			
			# ~ CALCULOS PARA DATOS REFERENTES A LAS UTILIDADES
			
			#variacion actual con respecto al mes anterior
			mes_act_ayo_act_uti = variacion_dif(datos_mes_act_ayo_act[0]['util'] , datos_mes_ant_ayo_act[0]['util'])

			#variacion actual con respecto al año anterior
			ayo_act_uti = ResumenM.objects.filter(ayo=mes_ayo_act['ayo'], mes__lte=mes_ayo_act['mes']).aggregate(Sum('util'))['util__sum']
			ayo_ant_uti = retornar_num(ResumenM.objects.filter(ayo=mes_ayo_ant['ayo']).aggregate(Sum('util'))['util__sum'])
			ayo_act_uti = variacion_dif(ayo_act_uti, ayo_ant_uti)
			
			
			# ~ CALCULOS PARA DATOS REFERENTES A LAS SERVICIOS

			#variacion actual con respecto al mes anterior
			mes_act_ayo_act_serv = variacion_dif(datos_mes_act_ayo_act[0]['serv'], datos_mes_ant_ayo_act[0]['serv'])
						
			#variacion actual con respecto al año anterior
			ayo_act_serv = ResumenM.objects.filter(ayo=mes_ayo_act['ayo'], mes__lte=mes_ayo_act['mes']).aggregate(Sum('serv'))['serv__sum']
			ayo_ant_serv = retornar_num(ResumenM.objects.filter(ayo=mes_ayo_ant['ayo']).aggregate(Sum('serv'))['serv__sum'])
			ayo_act_serv = variacion_dif(ayo_act_serv, ayo_ant_serv)
			
			
			# ~ CALCULOS PARA DATOS REFERENTES A LOS GASTOS
			
			#variacion mensual
			tmp_ant                = retornar_num(FacturasM.objects.filter(fhfactu__year=mes_ant['ayo'], fhfactu__month=mes_ant['mes']).aggregate(Sum('total'), Sum('transp')))
			tmp_act                = retornar_num(FacturasM.objects.filter(fhfactu__year=mes_ayo_act['ayo'], fhfactu__month=mes_ayo_act['mes']).aggregate(Sum('total'), Sum('transp')))
			mes_act_ayo_act_gastos = variacion_dif(retornar_num(tmp_act['total__sum']), retornar_num(tmp_ant['total__sum']))
			mes_act_ayo_act_transp = variacion_dif(retornar_num(tmp_act['transp__sum']), retornar_num(tmp_ant['transp__sum']))
			print(mes_act_ayo_act_gastos)
			print(mes_act_ayo_act_transp)
			# variacion anual
			tmp_ant = retornar_num(FacturasM.objects.filter(fhfactu__year=mes_ayo_ant['ayo']).aggregate(Sum('total'), Sum('transp')))
			tmp_act = retornar_num(FacturasM.objects.filter(fhfactu__year=mes_ayo_act['ayo'], fhfactu__month=mes_ayo_act['mes']).aggregate(Sum('total'), Sum('transp')))
			
									
			datos_mensuales.append({'mes': mes[mes_ayo_act['mes']],
									'clientes_totales' : datos_mes_act_ayo_act[0]['ncli_t'], #total de clientes totales
									'clientes_mes'     : clientes_mes, #total de clientes del mes
									'clientes_anual'   : clientes_anual, #variacion de clientes con respecto al mismo mes pero del año anterior
									'adquirieron'      : datos_mes_act_ayo_act[0]['ncli_a'], #total de clientes que adquirireron productos
									'gasto_mes'        : gasto_mes, #total adquirido, en unidad monetaria
									'ped_soli_mes'     : ped_soli_mes, #total de presupuestos solicitados en el mes
									'ped_vend_mes'     : ped_vend_mes, #total de presupuestos vendidos en el mes
									'ped_canc_mes'     : ped_canc_mes, #total de presupuestos cancelados en el mes
									'ped_proc_mes'     : ped_proc_mes, #total de presupuestos en proceso en el mes
									'ped_vend_anual'   : ped_vend_anual, #total de presupuestos en proceso en el mes
									'venta_proyectada' : venta_proyectada,
									'venta_por_aprobar': venta_por_aprobar,
									'venta_cancelada'  : venta_cancelada,
									'venta_efectiva'   : venta_efectiva,
									'num_personal'     : num_personal,
									'produccion_per_mes_act_ayo_act'    : produccion_per_mes_act_ayo_act, #produccion el mes actual y año actual
									'produccion_per_ayo_act'            : produccion_per_ayo_act,#produccion del año actual
									'mes_act_ayo_act_uti'          : mes_act_ayo_act_uti,
									'ayo_act_uti'                  : ayo_act_uti,
									'mes_act_ayo_act_serv'         : mes_act_ayo_act_serv,
									'ayo_act_serv'                 : ayo_act_serv,
									'mes_act_ayo_act_gastos'       : mes_act_ayo_act_gastos,
									'mes_act_ayo_act_transp'       : mes_act_ayo_act_transp,
									'invertido'       : mes_act_ayo_act_gastos['valor']+mes_act_ayo_act_transp['valor'],
									})
			if mes_ayo_act['mes'] == i['mes']:
				datos_mes_actual = datos_mensuales[-1]
				# ~ print(datos_mes_actual)
				
	ayos=[]
	for i in ResumenM.objects.order_by('ayo').values('ayo').distinct():
		ayos.append(i['ayo'])
		
	contexto = {
		'ayos'			  : ayos,
		'periodo'         : mes_ayo_act['ayo'],
		'mes'	          : mes[mes_ayo_act['mes']],
		'datos_mes_actual': datos_mes_actual,
		'mensual'         : datos_mensuales,
	}
	return render(request,'resumen_ventas.html', contexto)	


def estado( request, idventa, estado ):
	if request.method == 'POST':
		# ciclo del producto
		   # ~ 0-. POR_APROBACION, se envia el presupuesto al cliente.Se espera 
								   # ~ por la cancelación del inicio de trabajo (50% de adelanto)
		   # ~ 1-. EN_PROCESO, creación del producto.
		   # ~ 2-. EN_RUTA,producto se envio para la entrega. 
		   # ~ 3-. ENTREGADO.
				  # ~ ( MEJORA: en este punto la persona que realiza la entrega deberia ingresar al sistema y
						# ~ actualizar el estado a ENTREGADO).
				  # ~ El sistema deberá emitir un correo con una encuesta de satisfaccion al cliente. 
		# ~ 99-. CANCELADO, orden cancelada, el cliente no aprobo el producto
		estado  = int(request.POST['estado'])
		# ~ idventa = request.POST['idventa']
		# ~ print(estado)
		if estado > -1 and estado < 3:
			# ~ 0: POR_APROBACION
			# ~ 1: EN_PROCESO
			# ~ 2: EN_RUTA
			estado = estado + 1
		else: 
			if estado == 3:
				# ~ 3: ENTREGADO
				estado = 3
				
			else: 
				# ~ 99: CANCELADO
				estado = 99

		# ~ print(estado)

		VentasM.objects.filter(id=idventa).update(estado=estado)
		datos    = VentasM.objects.filter(id=idventa).values()
		fecha    = datos[0]['fhacd']
		cantidad = float(datos[0]['cant'])
		if estado == 1:
			# se actualiza datos del producto vendido
			r = ResumenM.objects.filter(ayo = fecha.year, mes = fecha.month).values()
			print(r[0])
			ResumenM.objects.filter(ayo = fecha.year, mes = fecha.month).update(
							npedv = r[0]['npedv'] + 1,
							nprdv = r[0]['nprdv'] + cantidad,
							tota  = r[0]['tota'] + float(datos[0]['costo']),
							util  = r[0]['util'] + float(datos[0]['utlds']),
							insm  = r[0]['insm'] + float(datos[0]['insm']),
							mate  = r[0]['mate'] + float(datos[0]['mate']),
							pers  = r[0]['pers'] + float(datos[0]['pers']),
							serv  = r[0]['serv'] + float(datos[0]['serv']), 
							)
			
			
			# ~ # se actualiza el numero de pedidos vendidos
			# ~ npedv = ResumenM.objects.filter(ayo = fecha.year).filter(mes = fecha.month).values('npedv')[0]['npedv']	
			# ~ ResumenM.objects.filter(ayo = fecha.year).filter(mes = fecha.month).update(npedv = int(npedv) + 1)
			# ~ # se actualiza el numero de productos vendidos
			# ~ nprdv = ResumenM.objects.filter(ayo = fecha.year).filter(mes = fecha.month).values('nprdv')[0]['nprdv']	
			# ~ ResumenM.objects.filter(ayo = fecha.year).filter(mes = fecha.month).update(nprdv = int(nprdv) + cantidad)	
		
		if estado == 99:
			npedc = ResumenM.objects.filter(ayo = fecha.year).filter(mes = fecha.month).values('npedc')[0]['npedc']	
			ResumenM.objects.filter(ayo = fecha.year).filter(mes = fecha.month).update(npedc = int(npedc) + 1)	
		
		return redirect('inicio_principal')
	
	if request.method == 'GET':
		
		contexto = {
			'idventa': idventa,
			'estado': estado,
			}
	
	
	return render(request,'estado_ventas.html', contexto)
