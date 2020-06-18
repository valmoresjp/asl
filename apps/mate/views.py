from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import datetime
from apps.mate.forms import InsumosF
from apps.mate.models import InsumosM
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):
	regs = InsumosM.objects.all()
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
def agregar(request):
	# print("dentor de agregar insumos")
	# print(request.POST['fingso'])
	if request.method == 'POST':
		# d = datetime.strptime(request.POST['fingso'], '%d-%m-%Y %H:%M')
		# print(d.strftime('%m/d/%Y %H:%M'))
		# print(request.POST['fingso'])
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
		else:		
			print("Error al guardar en la base de datos")
			return render(request,'errores_020819.html',{'form': form})
		return redirect ('inicio_mate')
	else:
		# fingso = datetime.now().strftime("%d-%m-%y %H:%M")
		# factu1 = fingso
		# form = Insumo(initial={'fingso': fingso, 'factu1': factu1})
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
