from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse

from django.db.models import Q

from datetime import datetime
# ~ from django.db import models, migrations
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
# Create your views here.

# ~ PROCESO PARA MIGRAR LOS DATOS ENTRE BASE DE DATOS

	# ~ BD con datos(estructura vieja y con datos) --> hacia BD nueva (nueva estructura y sin datos)
# ~ NOTA: se debe realizar respaldo de la base de datos que contiene los valores que se desean mantener(estructura vieja)
 
# ~ 1-. El proceso consiste en agregar los campos nuevos a la base de datos vieja.
	# ~ Esto con el objetivo de mantener los indices.
	# ~ EL COMO:  
			# ~ 1-. Leer la base de datos con la nueva estructura y extraer los nombre de los campos. 
			# ~ 2-. Leer la base de datos con la vieja estructura y extraer los nombre de los campos.
			# ~ 3-. Comparar ambos resultados y agregar los campos de la nueva estructura a la vieja estructura
			 
# ~ 2-. Se procede a agregar los valores a los campos nuevos, esto es en el caso de: 
     # ~ --- Si el campo en cuestion cambia de nombre
     # ~ --- Si el campo es igual a un valor o combinancion de varios valores
     
# ~ 3-. Eliminar los campos de la estructura vieja que no se encuentren en la estructura nueva.


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def migrar(request):
	bd_actual = "actual"
	bd_nueva = "definitiva"
	# ~ apps = []
	tablas = []
	print("Obteniendo las tablas configuradas en el sistema ...")
	for i in settings.INSTALLED_APPS:
		if i.startswith('apps.'):
			aplicacion = i.split('.')[1]
			for  k in ContentType.objects.filter(app_label=aplicacion).values('model'):
				tbl = aplicacion + "_" + k['model']
				tablas.append(tbl)

	print("Creando Base de datos definitiva....")
	# duplicar la base de datos actual
	from shutil import copy as cp
	cp("actual.sqlite3", "definitiva.sqlite")
	
	print("\rCreada")
	
	# ~ print("Obteniendo estructura de la nueva BD...")
	# ~ modelo = apps.get_app_config("clientes")
	
	from django.db import connections

	BDA ={}
	with connections[bd_actual].cursor() as cursor:
		a = cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
		for row in dictfetchall(cursor):
			for i in tablas:
				if i.startswith(row['tbl_name']):
					campos = []
					n =row['sql'].find("(")
					for k in  row['sql'][n+1:len(row['sql'])-1].split(","):
						dd =k.strip().split(" ")
						d = {'campo':dd[0].replace('"',""), 'tipo':  k[len(dd[0])+1:].strip()}
						campos.append(d)
					# ~ BDA[row['tbl_name']] = campos
						clave = row['tbl_name'] + "."+d['campo']
						BDA[clave] = d['tipo']

	# ~ print(BDA)
	# ~ for i in BDA['clientes_referidosm']:
		# ~ print(i)
		
	
	# ~ print(BDA['clientes_referidosm'])
		
	BDN ={}
	lista_act=""
	with connections[bd_nueva].cursor() as cursor:
		a = cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
		for row in dictfetchall(cursor):
			for i in tablas:
				lista_act=""
				if i.startswith(row['tbl_name']):
					campos = []
					n =row['sql'].find("(")
					for k in  row['sql'][n+1:len(row['sql'])-1].split(","):
						dd =k.strip().split(" ")
						d = {'campo':dd[0].replace('"',""), 'tipo':  k[len(dd[0])+1:].strip()}
						lista_act = lista_act + " " + d['campo']
						campos.append(d)
					# ~ BDN[row['tbl_name']] = campos
						clave = row['tbl_name'] + "."+d['campo']
						BDN[clave] = d['tipo']

	print(BDN)
	BDD = {}
	for campo,tipo in BDA:
		if campo in BDN:
			print("Existe en ambas")
			if tipo == BDN[campo]:
				print(" sin cambios en el tipo de dato")
			else:
				print("Tipo de dato diferente. se debe modificar el tipode dato")
		else:
			print("No existe en BDN. Se debe borrar este campo") 
	
	# ~ for tbl in tablas:
		# ~ print("Analizando.....",tbl)
		# ~ if tbl in BDA:
			# ~ if tbl in BDN:
				# ~ print("Tabla existe en ambas BD. Verificando campos....")
				# ~ for campo_act in BDA[tbl]:
					# ~ for campo_nev in BDN[tbl]:
						# ~ if campo_act['campo'] == campo_nev['campo']:
			# ~ else:
				# ~ print("Tabla no existe en BDN. Eliminado tabla de la nueva base de datos..."
		# ~ else:
			# ~ print("Eliminar ....",tbl)


	
	# ~ bd_actual = InsumosM.objects.using('default').all()
	return render (request,'inicio_migrar.html')
