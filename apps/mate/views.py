from django.shortcuts import render , redirect
from django.http import HttpResponse
import mimetypes
from django.conf import settings
from django.db.models import Avg, Min, Max, Sum
from django.db.models import Q

from datetime import datetime, date
from apps.mate.forms import InsumosF, ComprasF, FacturasF,PersonalF
from apps.mate.models import InsumosM, ComprasM, FacturasM
from django.contrib.auth.decorators import login_required
# Create your views here.
from django import template

register = template.Library()

@register.filter
def cambio_sig(value, arg):
    return value * (-1)



def inicio(request):
	listado = {
				'MAT':'MATERIAL',
				'PER':'PERSONAL',
				'MYH':'MAQUINAS Y HERRAMIENTAS',
				'SER':'SERVICIO',
				'ING':'INGREDIENTE',
				}
	if request.method == 'POST':
		clave = request.POST['tipo']
		if clave == "NNN":
			clave = "ING"
		regs = InsumosM.objects.filter(tipo=clave).order_by('inven')
	
	if request.method == 'GET':
		clave = 'ING'
		regs = InsumosM.objects.filter(tipo=clave).order_by('inven')
			
	# ~ print(	listado[clave])
	contexto = {
		'regs': regs,
		'listado':listado[clave],
		'tipo'   : clave,
		}
	return render (request,'inicio_mate.html',contexto )

@login_required(login_url='/inicio/ingreso')	
def agregar(request, idfactu):

	if request.method == 'POST':

		form = InsumosF(request.POST)
		if form.is_valid(): # and not error:
			instancia = form.save(commit=False)
			instancia.cumedcal = (instancia.costop + instancia.costot)/instancia.cantd
			form.save()

			# se obtiene el insumo almacenado para obtener la informacipon y registrar la factura
			insm = InsumosM.objects.filter(codigo=request.POST['codigo']).filter(descrip=request.POST['descrip'])
			
			compras = {
				'idinsm'  :insm[0].id, 
				'umedida' :insm[0].umedida,
				'costop'   :insm[0].costop,
				'costot'   :insm[0].costot,
				'cantd'   :insm[0].cantd,
				'idfactu'  :idfactu,
				'fhcomp'  :date.today().strftime("%d-%m-%Y")	,
			}
			comprasf = ComprasF(compras)
			if comprasf.is_valid():	
				comprasf.save()
				# ~ se actualiza los costos de transporte porque se agrego otro item
				ComprasM.objects.filter(idfactu = idfactu).update(costot=compras['costot'])
			else:
				print("Error al almacenar factura")
				InsumosM.objects.get(id=insm.id).delete()
			
			return redirect('contenido_factura_mate',idfactu)
			
		else:		
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
		return redirect (url)
	else:
		
		registro = FacturasM.objects.filter(id=idfactu).values()[0]
		if registro['codigo'].startswith("PER-"):
			i = {
					'codigo' : registro['codigo'],
					'umedida': 'HH',			
					'cantd'  : 1,
					'inven'  : 1,
					'tipo'   : 'PER',		
					'costop' : registro['total'],
					'costot' : 0.0
				}
			form = InsumosF(initial=i) 
		else:
			total_transporte = FacturasM.objects.filter(id=idfactu)[0].transp
			nprod = ComprasM.objects.filter(idfactu = idfactu).count()
			
			costo_transporte = total_transporte/(nprod + 1)
			form = InsumosF(initial={'costot': costo_transporte}) 
	return render( request, 'agregar_mate.html', {'codigo': registro['codigo'],'form':form})
	
	
@login_required(login_url='/inicio/ingreso')	
def editar(request,idinsm):

	insumo = InsumosM.objects.get(id=idinsm)
	if request.method == 'GET':
		form = InsumosF(instance=insumo)
	else:
		form = InsumosF(request.POST, instance=insumo)
		if form.is_valid():
			form.save()
		return redirect('inicio_mate') 
	return render(request,'agregar_mate.html', {'form':form})

@login_required(login_url='/inicio/ingreso')
def eliminar(request, idinsm):

	if request.method == 'POST':
		url_ant = "inicio_mate"
		insumo = InsumosF.objects.get(id=idinsm)
		insumo.delete()
		return redirect(url_ant)
	else:
		insumo = InsumosM.objects.get(id=idinsm)
	
	return render(request, 'eliminar_mate.html',{'reg':insumo})

def compras_mate(request,idinsm):
	datos = []
	insm = InsumosM.objects.get(id=idinsm)
	compras = ComprasM.objects.filter(idinsm=idinsm)
	for i in compras:
		factura = FacturasM.objects.get(id=i.idfactu)
		print(i.costop, "  ", i.costot,"  ",i.cantd,"    ",i.cumedida())
		datos.append({
						'id'             : i.id,
						'cumedida'       : i.cumedida(),
						'costop'         : i.costop,
						'costot'         : i.costot,
						'cantidad'       : i.cantd,
						'idfactura'      : factura.id,
						'numero_factura' : factura.codigo,
						'fecha_compra'   : i.fhcomp,
						'factura'        : factura.archivo.name,
						})
	
	res = ComprasM.objects.filter(idinsm=idinsm).aggregate(precio_avg=Avg('costop'), precio_min=Min('costop'), precio_max=Max('costop'))
	contexto = {
				'insm':insm,
				'compras':datos,
				'minimo': res['precio_min'],
				'maximo': res['precio_max'],
				'promedio': res['precio_avg'],
				}
	return render(request, 'compras_mate.html', contexto)
	
def agregar_factura(request,tipo):
	
	if request.method == 'POST':
		form = FacturasF(request.POST,request.FILES)
		if form.is_valid():
			# file is saved
			instancia = form.save(commit=False)
			## verificar que el archivo haya sido ingresado
			instancia.archivo.name = str(instancia.numero) + instancia.fhfactu.strftime("_%d%m%Y")
			instancia.codigo = tipo + "-" + str(instancia.codigo)
			form.save()

			return redirect('listar_factura_mate', tipo)
		else:
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
	else:
		print('DATOS: ',request.GET)
		form = FacturasF()
	return render(request, 'agregar_facturas_mate.html', {'form': form})#, 'datos':datos})

def descarga_factura(request,idfactu):#idfactu):

	factura =FacturasM.objects.get(id=idfactu)
	ruta = settings.MEDIA_ROOT + factura.archivo.url
	nombre =  ruta.split("/")[-1]
	fl = open(ruta, 'rb')
	mime_type, _= mimetypes.guess_type(ruta)
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % nombre

	return response
	
def listar_factura(request, tipo):
	
	if tipo == "TOD":
		facturas = FacturasM.objects.order_by('-fhfactu')
	else: 
		facturas = FacturasM.objects.filter(codigo__startswith=tipo).order_by('-fhfactu')
		
	contexto = {
		'facturas' : facturas,
		'tipo'     : tipo,
		}
	print(tipo,"  --- ",)
	return render(request, 'listar_factura_mate.html', contexto)#, 'datos':datos})

def listar_personal(request):
	contexto = {
		'facturas' : FacturasM.objects.order_by('-fhfactu'),
		}
	return render(request, 'listar_personal_mate.html', contexto)#, 'datos':datos})

def agregar_personal(request):
	print('Agregar personal')

	if request.method == 'POST':
		# ~ print('Ingreso a guardar personal')
		form = FacturasF(request.POST,request.FILES)
		if form.is_valid():
			instancia = form.save(commit=False)
			## verificar que el archivo haya sido ingresado
			instancia.archivo.name = str(instancia.numero) + instancia.fhfactu.strftime("_%d%m%Y")
			# ~ print(instancia.codigo, "   ", instancia.id)
			form.save()
			registro = FacturasM.objects.filter(codigo=instancia.codigo).values('codigo','id')[0]
			# ~ print(registro)
				
			return redirect('agregar_mate',registro['id'])
		else:
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
	else:
		print('DATOS: ',request.GET)
		personal = int( FacturasM.objects.filter(codigo__startswith='PER').order_by('-codigo').values('codigo')[0]['codigo'][4:])
		codigo   = 'PER-' + str(personal + 1).zfill(4)
		emisor   = 'ASL'
		numero   = 191 
		print(codigo)
		form = PersonalF(initial={'codigo':codigo, 'emisor':emisor, 'numero':numero})
	return render(request, 'agregar_personal_mate.html', {'form': form})#, 'datos':datos})

def contenido_factura(request, idfactu):
	
	
	if request.method == 'POST':
		# se verifica si el item existe
		idinsm = request.POST['items'].split("_")[0]
		if idinsm.isdigit() == False:
			idinsm=-1
		
		if InsumosM.objects.filter(id=idinsm).exists():
			return redirect('item_factura_mate',idfactu,idinsm)
		else:
			print("No existe insumo")
			return redirect('agregar_mate',idfactu)
	
	else:
		datos = []
		factura = FacturasM.objects.get(id=idfactu)
		insumos = InsumosM.objects.all()
		total_agregado = 0
		for i in ComprasM.objects.filter(idfactu=idfactu):
			insm = InsumosM.objects.get(id=i.idinsm)
			datos.append( {
							'idinsm'      : i.idinsm,
							'descripcion' : insm.descrip,
							'umedida'     : insm.umedida,
							'costop'       : i.costop,
							'costot'       : i.costot,
							'costo'       : i.ctotal(),
							'cantidad'    : i.cantd,
							})
			total_agregado = total_agregado + i.ctotal()
		
		contexto = {
			'factura': factura,
			 'datos' : datos,	 
			 'items' : insumos,
			 'total_agregado': total_agregado,
		}
	return render(request,'contenido_factura_mate.html',contexto)
	
def detalle_factura(request, idfactu):
	
	if request.method == 'POST':
		# se verifica si el item existe
		idinsm = request.POST['items'].split("_")[0]
		if idinsm.isdigit() == False:
			idinsm=-1
		
		if InsumosM.objects.filter(id=idinsm).exists():
			return redirect('item_factura_mate',idfactu,idinsm)
		else:
			print("No existe insumo")
			return redirect('agregar_mate',idfactu)
	
	else:
		datos = []
		factura = FacturasM.objects.get(id=idfactu)
		insumos = InsumosM.objects.all()
		total_agregado = 0
		for i in ComprasM.objects.filter(idfactu=idfactu):
			insm = InsumosM.objects.get(id=i.idinsm)
			datos.append( {
							'idinsm'      : i.idinsm,
							'descripcion' : insm.descrip,
							'umedida'     : insm.umedida,
							'costop'       : i.costop,
							'costot'       : i.costot,
							'costo'       : i.ctotal(),
							'cantidad'    : i.cantd,
							})
			total_agregado = total_agregado + i.ctotal()
		
		contexto = {
			'factura': factura,
			 'datos' : datos,	 
			 'items' : insumos,
			 'total_agregado': total_agregado,
		}
	return render(request,'detalle_factura_mate.html',contexto)
	
def agregar_item_factura(request, idfactu):
	pass
	contexto={}
	return(render,"agregar_item_factura.html", contexto)	
	
def item_factura(request, idfactu,idinsm):
	
	if request.method == 'POST':
		
		form = ComprasF(request.POST)
		if form.is_valid():
			form.save()
			a = InsumosM.objects.get(id=request.POST['idinsm'])
			
			cumedida_anterior = a.cumedcal
			cumedida_actual = (float(request.POST['costop']) + float(request.POST['costot']))/float(request.POST['cantd']) 
			
			if cumedida_anterior > cumedida_actual:
				cumedida_actual = (cumedida_anterior + cumedida_actual)/2
			
			# Para un cálculo más preciso se debe dividir la diferencia "cumedida_actual - cumedcal" entre el inventario existente
			# asi de esta forma esa diferencia se compensa con la cantidad de producto adquirido a un nuevo precio
						
			inventario = float(a.inven)+ float(request.POST['cantd'])
			c = InsumosM.objects.filter(id=request.POST['idinsm']).update(inven=inventario)
			

			## NOTA: cada vez que se realice una compra se debe tener en cuenta que los precios pueden variar
			##       por lo que el precio de compra anterior puede diferir y puede ser para perdida, ya que,
			##       si se compro más barato que la vez anterior y aún existen productos en el inventario
			##       el costo actual del producto será sustituido por el ultimo calculado.
			##       Por lo tanto hay que buscar una forma de mantener el precio hasta que se agote la
			##       existencia de la compra mas costosa, o buscar un precio que corrija esta diferencia.
			
			##       Una posible solución es de fijar una referencia, por ejemplo, el costo del producto 
			##       al detal y a partir de alli verificar la diferencia o determiar el precio a partir del 
			##       resultado del promedio de:
			##
			##        PRECIO_DE_REFERENCIA
			##        PRECIO_DE_COMPRA_ANTERIOR
			##        PRECIO_DE COMPRA_ACTUAL 
			c = InsumosM.objects.filter(id=idinsm).update(cumedcal=cumedida_actual,cantd=request.POST['cantd'],costop=request.POST['costop'], costot=request.POST['costot'])
			ComprasM.objects.filter(idfactu = idfactu).update(costot=request.POST['costot'])

			return redirect('contenido_factura_mate', idfactu=idfactu )
		else:
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
	else:
		
		form = ComprasF()

		total_transporte = FacturasM.objects.filter(id=idfactu)[0].transp
		nprod = ComprasM.objects.filter(idfactu = idfactu).count()
		costo_transporte = total_transporte/(nprod + 1)

		# ~ form = InsumosF(initial={'costot': costo_transporte})
		insumo = InsumosM.objects.get(id=idinsm)
		f = date.today()
		fecha = f.strftime("%d-%m-%Y")
		datos ={
				'idinsm': insumo.id,
				'umedida': insumo.umedida,
				# ~ 'costo': insumo.max(),
				'costop': 0,
				'costot': costo_transporte,
				# ~ 'cantd':insumo.cantd,
				'cantd':0,
				'descrip':insumo.descrip,
				'idfactu':idfactu,#FacturasM.objects.get(id=idfactu).numero,
				'fhcomp':fecha,
			}
		form = ComprasF(datos)
		form.fields['umedida'].widget.attrs['readonly'] = True
		form.fields['idinsm'].widget.attrs['readonly'] = True
		form.fields['idfactu'].widget.attrs['readonly'] = True
		# ~ form.fields['nfactu'].widget.attrs['visible'] = False
		# ~ form.fields['archivo'].required = False
		# ~ form.fields['fhcomp'].required = False
	return render(request, 'item_factura_mate.html', {'form': form})#, 'datos':datos})
