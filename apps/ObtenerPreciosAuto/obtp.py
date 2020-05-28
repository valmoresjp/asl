

from bs4 import BeautifulSoup
import requests
import re

URL =  "https://www.telemercados.cl/harina-selecta-con-polvos-1kg/p"
etiqueta = 'strong'
clase = 'skuBestPrice'
# Realizamos la petición a la web
req = requests.get(URL)

# Comprobamos que la petición nos devuelve un Status Code = 200
status_code = req.status_code
if status_code == 200:

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(req.text, "html.parser")

    # Obtenemos todos los divs donde están las entradas
    valor = html.find(etiqueta, {'class': clase }).getText()
    
    valor = float(valor.lstrip("$").replace(",","."))
    valor = "{0:.2f}".format(valor)
    print(valor)

    # Recorremos todas las entradas para extraer el título, autor y fecha


else:
    print ("Status Code %d", status_co)
