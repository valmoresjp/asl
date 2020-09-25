from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import json
from apps.mate.models import InsumosM
from apps.partida.models import PartidasM, PartidaDetallesM
from apps.prod.models import ProductosM, PartidasPRDM, MaterialesM, ServiciosM, PersonalM, ImagenesM#, MaquiyHerraM, CstsAdnlsM, 
from apps.prod.forms import ProductosF, ImagenesF#, VentasF
from apps.conf.models import CostosDescripcionM, UtilidadesDetallesM, UtilidadesM
from apps.clientes.models import ClientesM
from django.db.models import Q

from PIL import Image


from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):

	obj = ProductosM.objects.all().order_by('-fhcrea')
	contexto = {
				'obj': obj,
	            }
	
	return render (request,'inicio_producto-1.html', contexto)

@login_required(login_url='/inicio/ingreso')
def nuevo(request):
	# ~ print(request.POST)
	if request.method == 'POST':
		form = ProductosF(request.POST)
		if form.is_valid():
			form.save()
			# ~ print (form)
			# ~ img_form = ImagenesM.objects.create(idprod=form.id)
		else:
			return render(request,'errores.html',{'form': form})

		return redirect ('inicio_producto')
	else:
		form = ProductosF()
	return render(request,'nuevo_producto.html', {'form': form})

@login_required(login_url='/inicio/ingreso')
def imagenes(request, idprod):
	
	if request.method == 'POST':
		imagenes=ImagenesM.objects.get(idprod=idprod)
		form  = ImagenesF(request.POST, request.FILES, instance=imagenes)
		if form.is_valid():
			form.save()

			for clave,valor in request.FILES.items():
				nombre = '{}{}{}{}'.format( settings.BASE_DIR,settings.MEDIA_URL,'imagenes/',valor)
				nuevo = '{}{}{}{}{}'.format( 'imagenes/',idprod,'-',clave,'.jpg')
				img = Image.open(nombre)
				new_img = img.resize((350,450))
				if clave == 'img1':
					ImagenesM.objects.filter(idprod=idprod).update(img1=nuevo)
				if clave == 'img2':
					ImagenesM.objects.filter(idprod=idprod).update(img2=nuevo)
				if clave == 'img3':
					ImagenesM.objects.filter(idprod=idprod).update(img3=nuevo)
				if clave == 'img4':
					ImagenesM.objects.filter(idprod=idprod).update(img4=nuevo)
				new_img.save('{}{}{}'.format(settings.BASE_DIR,settings.MEDIA_URL,nuevo))
		else:
			return render(request,'errores.html',{'form': form})

		return redirect ('detallar_producto',idprod)
	else:
		a = ImagenesM.objects.filter(idprod=idprod)
		if not a.exists():
			a = ImagenesM.objects.create(idprod=idprod)
		a = ImagenesM.objects.get(idprod=idprod)
		form = ImagenesF(instance=ImagenesM.objects.get(idprod=idprod))

	return render(request,'imagenes_producto.html', {'form': form, 'imagen':a})

@login_required(login_url='/inicio/ingreso')
def editar(request, idprod ):
	producto = ProductosM.objects.get(id=idprod)
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
	a = ImagenesM.objects.filter(idprod=idprod)
	if not a.exists():
		a = ImagenesM.objects.create(idprod=idprod)
	# ~ a = ImagenesM.objects.get(idprod=idprod)
		
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
					PartidasPRDM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()
					
			if i['destino'] == "Materiales":
				if i['accion'] == 'actualizar':	
					# ~ El registro existe y se actualiza
					a = MaterialesM.objects.filter(idprd=idprod).filter(idmate=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = MaterialesM(idmate=i["id"], idprd=idprod, cant=i["datos"])
					g.save()					
				if i['accion'] == 'eliminar':
					MaterialesM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()				
				
			if i['destino'] == "Servicios":
				if i['accion'] == 'actualizar':
					# ~ El registro existe yf se actualiza
					ServiciosM.objects.filter(idprd=idprod).filter(idserv=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = ServiciosM(idserv=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
					ServiciosM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()		
			
			if i['destino'] == "Personal":
				if i['accion'] == 'actualizar':
					# ~ El registro existe y se actualiza
					PersonalM.objects.filter(idprd=idprod).filter(idpers=i["id"]).update(cant=i["datos"])
				if i['accion'] == 'nuevo':
					# ~ El registro no existe, se crea un nuevo registro
					g = PersonalM(idpers=i["id"], idprd=idprod, cant=i["datos"])
					g.save()
				if i['accion'] == 'eliminar':
					PersonalM.objects.filter(idprd=idprod).filter(id=i["id"]).delete()		
			
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
	
		return redirect(url)
		
	if request.method == 'GET':
		for i in PartidasPRDM.objects.filter(idprd=idprod):
			if PartidasM.objects.filter(id = i.idpart).exists() == True:
				part = PartidasM.objects.get(id = i.idpart)		
				pdatos.append(	
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
		
		for i in MaterialesM.objects.filter(idprd=idprod):
			if InsumosM.objects.filter(tipo="MAT").filter(id = i.idmate).exists() == True:
				mate = InsumosM.objects.get(id = i.idmate)
				mdatos.append(	
					{'id':       i.id,  
					 'idmate':   mate.id,  
					 'nombre':   mate.descrip,
					 'umedida':  mate.umedida,
					 'cumedida': mate.cumedida,
					 'cantidad': i.cant,
					 'costo':    round(mate.cumedida()*i.cant,2)
				})
				total = total + mate.cumedida()*i.cant
		totales["materiales"] = round(total,2)
		totprd = totprd + total
		total = 0.0
					
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
					})
				total = total + pers.cumedida()*i.cant
		totales["personal"] = round(total,2)
		totprd = totprd + total
		total = 0.0
		totales['totprd'] = round(totprd,2)
		
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
	contexto['imagenes']   = ImagenesM.objects.get(idprod=idprod)
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
	
def presupuesto(request, idprod):
# ~ def categoria_print(self, pk=None):  
	import io 
	from reportlab.lib.pagesizes import A4, letter
	from reportlab.pdfgen import canvas 
	from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle  
	from reportlab.lib.styles import getSampleStyleSheet  
	from reportlab.lib import colors  
	from reportlab.platypus import Table
	from PIL import Image
	
	
	response = HttpResponse(content_type='application/pdf')
	buff = io.BytesIO()  
	doc = SimpleDocTemplate(buff,  
               pagesize=letter,  
               rightMargin=40,  
               leftMargin=40,  
               topMargin=60,  
               bottomMargin=18,  
               )  

	w, h = A4
	pdf = canvas.Canvas(buff, pagesize=A4)
	
	### Cabecera
	pdf.drawImage("/media/svjsp/Respaldos/Personales/Proyectos/v300320/v3.1/v01a/static/antojos_bn_112.svg", 50, h - 200, width=150, height=150)
	
	#####
	
	pdf.drawString(50, h - 50, "¡Hola, mundo!")
	pdf.showPage()
	pdf.save()
	pdf = buff.getvalue()
	response.write(pdf)  
	buff.close()
	
	return response  
