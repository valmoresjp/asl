from django.shortcuts import render , redirect
from django.http import HttpResponse
import mimetypes
from django.db.models import Avg, Min, Max

from datetime import datetime, date
from apps.mate.forms import InsumosF, ComprasF, FacturasF
from apps.mate.models import InsumosM, ComprasM, FacturasM
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):
	regs = InsumosM.objects.all().order_by('inven')
	idatos=[]
	for i in regs:
		# ~ print("Distribuidor	Costo	Costo/Umedida")
		a=""
		if i.cmedi1() > 0:
			a = i.distb1 + " , " + str(i.costo1).strip()+" , " + str(i.cmedi1()).strip() + "\n"
		if i.cmedi2() > 0:
			a = a + " , " +i.distb2 + " , " + str(i.costo2).strip()+" , " + str(i.cmedi2()).strip() + "\n"
		if i.cmedi3() > 0:
			a = a + " , " +i.distb3 + " , " + str(i.costo3).strip()+" , " + str(i.cmedi3()).strip() + "\n"
		if i.cmedi4() > 0:
			a = a + " , " +i.distb4 + " , " + str(i.costo4).strip()+" , " + str(i.cmedi4()).strip() + "\n"
		if i.cmedi5() > 0:
			a = a + " , " + i.distb5 + " , " + str(i.costo5).strip()+" , " + str(i.cmedi5()).strip() + "\n"
			
		idatos.append(	
					{'id'            : i.id,
					 'codigo'        : i.codigo,  
					 'descripcion'   : i.descrip,
					 'cantidad'      : i.cantd,
					 'umedida'       : i.umedida,
					 'costo'         : i.max(),
					 'cumedida'      : i.cumedida,
					 'inventario'    : i.inven,
					 'distribuidores': a,
					 'tipo'          : i.tipo
					})
					
					
	return render (request,'inicio_mate.html',{'regs': idatos})

@login_required(login_url='/inicio/ingreso')	
def agregar(request, idfactu):

	if request.method == 'POST':

		f = [-1,-1,-1,-1,-1]
		error = False

		if len(request.POST['distb2'].strip())>0 and float(request.POST['costo2'])>=0.0 :
				f[1] = datetime.now()
		if len(request.POST['distb3'].strip())>0 and float(request.POST['costo3'])>=0.0 :
				f[2] = datetime.now()
		if len(request.POST['distb4'].strip())>0 and float(request.POST['costo4'])>=0.0 :
				f[3] = datetime.now()
		if len(request.POST['distb5'].strip())>0 and float(request.POST['costo5'])>=0.0 :
				f[4] = datetime.now()
		for  i in (1,2,3,4):
			if f[i] == -1:
				error = False

		form = InsumosF(request.POST)
		if form.is_valid() and not error:
			instancia = form.save(commit=False)
			if f[1]!=-1:
				instancia.factu2 = f[1]
			if f[2]!=-1:
				instancia.factu3 = f[2]
			if f[3]!=-1:
				instancia.factu4 = f[3]
			if f[4]!=-1:
				instancia.factu5 = f[4]
			
			instancia.save()
			## se obtiene el insumo almacenado para obtener la informacipon y registrar la factura
			insm = InsumosM.objects.filter(codigo=request.POST['codigo']).filter(descrip=request.POST['descrip'])
			
			compras = {
				'idinsm'  :insm[0].id, 
				'umedida' :insm[0].umedida,
				'costo'   :insm[0].costo1,
				'cantd'   :insm[0].cantd,
				'nfactu'  :idfactu,
				'fhcomp'  :date.today().strftime("%d-%m-%Y")	,
			}
			comprasf = ComprasF(compras)
			if comprasf.is_valid():	
				comprasf.save()
			else:
				print("Error al almacenar factura")
				InsumosM.objects.get(id=insm.id).delete()
			
			return redirect('contenido_factura_mate',idfactu)
			
		else:		
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
		return redirect (url)
	else:
		form = InsumosF()
	return render( request, 'agregar_mate.html', {'form':form})
	
	
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
		factura = FacturasM.objects.get(id=i.nfactu)
		datos.append({
						'id'             : i.id,
						'idinsm'         : i.idinsm,
						'costo'          : i.costo,
						'cantidad'       : i.cantd,
						'idfactura'      : factura.id,
						'numero_factura' : factura.numero,
						'fecha_compra'   : i.fhcomp,
						'factura'        : factura.archivo.name,
						})
	
	res = ComprasM.objects.filter(idinsm=idinsm).aggregate(precio_avg=Avg('costo'), precio_min=Min('costo'), precio_max=Max('costo'))
	contexto = {
				'insm':insm,
				'compras':datos,
				'minimo': res['precio_min'],
				'maximo': res['precio_max'],
				'promedio': res['precio_avg'],
				}
	return render(request, 'compras_mate.html', contexto)
	
def agregar_factura(request):
	
	if request.method == 'POST':
		form = FacturasF(request.POST,request.FILES)
		if form.is_valid():
			# file is saved
			instancia = form.save(commit=False)
			## verificar que el archivo haya sido ingresado
			instancia.archivo.name = str(instancia.numero) + instancia.fhfactu.strftime("_%d%m%Y")
			form.save()
			# ~ else:
				
			return redirect('listar_factura_mate')
		else:
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
	else:
		
		form = FacturasF()
	return render(request, 'agregar_facturas_mate.html', {'form': form})#, 'datos':datos})

def descarga_factura(request,idfactu):#idfactu):
	# fill these variables with real values
	factura =FacturasM.objects.get(id=idfactu)
	
	ruta = factura.archivo.url
	print("DESCARGANDO FACTURAS: ", ruta)
	nombre = ruta.split("/")[-1]
	print("NOMBRE: ",nombre)
	fl = open(ruta, 'rb')
	# ~ fl = open(ruta, 'rb')
	mime_type, _= mimetypes.guess_type(ruta)
	print(mime_type)
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % nombre
	return response
	
def listar_factura(request):
	contexto = {
		'facturas' : FacturasM.objects.all()
		}
	return render(request, 'listar_factura_mate.html', contexto)#, 'datos':datos})

def contenido_factura(request, idfactu):
	
	if request.method == 'POST':
		print("POST.........")
		print(idfactu)
		# se verifica si el item existe
		idinsm = request.POST['items'].split("_")[0]
		
		if idinsm == "":
			idinsm=-1
		else:
			print(len(idinsm))
		
		if InsumosM.objects.filter(id=idinsm).exists():
			return redirect('item_factura_mate',idfactu,idinsm)
		else:
			print("No existe insumo")
			return redirect('agregar_mate',idfactu)
	
	else:
		print("POST.........")
		datos = []
		factura = FacturasM.objects.get(id=idfactu)
		print(factura.compra_total())
		insumos = InsumosM.objects.all()
		# ~ print(insumos)
		for i in ComprasM.objects.filter(nfactu=idfactu):
			insm = InsumosM.objects.get(id=i.idinsm)
			datos.append( {
							'idinsm'      : i.idinsm,
							'descripcion' : insm.descrip,
							'umedida'     : insm.umedida,
							'costo'       : i.costo,
							'cantidad'    : i.cantd,
							})
		
		contexto = {
			'factura': factura,
			 'datos' : datos,
			 'items' : insumos,
		}
	return render(request,'contenido_factura_mate.html',contexto)
	
def agregar_item_factura(request, idfactu):
	pass
	contexto={}
	return(render,"agregar_item_factura.html", contexto)	
	
def item_factura(request, idfactu,idinsm):
	
	if request.method == 'POST':
		# ~ f = request.POST['fhcomp'].split("-")
		# ~ fecha=f[2]+"-"+f[1]+"-"+f[0]
		# ~ print(request.POST['fhcomp'])
		# ~ print(fecha)
		
		form = ComprasF(request.POST)
		if form.is_valid():
			form.save()
			a = InsumosM.objects.get(id=request.POST['idinsm'])
			inventario = float(a.inven)+ float(request.POST['cantd'])
			c = InsumosM.objects.filter(id=request.POST['idinsm']).update(inven=inventario)
			
			print("Guardando el costo")
			res = ComprasM.objects.filter(idinsm=idinsm).aggregate(precio_avg=Avg('costo'), precio_min=Min('costo'), precio_max=Max('costo'))
			c = InsumosM.objects.filter(id=request.POST['idinsm']).update(costo1=res['precio_max'])
			
			# ~ url = 'factura/compras/' + str(idinsm) + '/' 
			# ~ return redirect('compras_mate', idinsm=idinsm )
			return redirect('contenido_factura_mate', idfactu=idfactu )
		else:
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
	else:
		
		form = ComprasF()
		
		insumo = InsumosM.objects.get(id=idinsm)
		f = date.today()
		fecha = f.strftime("%d-%m-%Y")
		datos ={
				'idinsm': insumo.id,
				'umedida': insumo.umedida,
				# ~ 'costo': insumo.max(),
				'costo': 0,
				# ~ 'cantd':insumo.cantd,
				'cantd':0,
				'descrip':insumo.descrip,
				'nfactu':idfactu,#FacturasM.objects.get(id=idfactu).numero,
				'fhcomp':fecha,
			}
		form = ComprasF(datos)
		form.fields['umedida'].widget.attrs['readonly'] = True
		form.fields['idinsm'].widget.attrs['readonly'] = True
		form.fields['nfactu'].widget.attrs['readonly'] = True
		# ~ form.fields['nfactu'].widget.attrs['visible'] = False
		# ~ form.fields['archivo'].required = False
		# ~ form.fields['fhcomp'].required = False
	return render(request, 'item_factura_mate.html', {'form': form})#, 'datos':datos})
