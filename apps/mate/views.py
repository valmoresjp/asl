from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import datetime
from apps.mate.forms import InsumosF
from apps.mate.models import InsumosM
from django.contrib.auth.decorators import login_required
# Create your views here.

def inicio(request):
	regs = InsumosM.objects.all()
	return render (request,'inicio_mate.html',{'regs': regs})

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
