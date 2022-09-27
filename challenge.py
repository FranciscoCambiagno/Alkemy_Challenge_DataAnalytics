from bs4 import BeautifulSoup
import csv
import requests
from decouple import config
import os
from datetime import date

def ObtenerCSV(urls):
    urls = list(map(PrepararURL, urls))
    
    for i, url in enumerate(urls):
        if i == 0:
            tipos_datos = "museos"
        elif i == 1:
            tipos_datos = "cines"
        else:
            tipos_datos = "bibliotecas"
        
        direccion = obtenerDireccion(tipos_datos)
        os.makedirs(direccion[0], exist_ok=True)

        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("table")
        for table in tables:
            with open(direccion[0] + direccion[1] + ".csv", "w", encoding='utf8') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
                wr.writerows([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])

def obtenerDireccion(datos):
    """
    Genera la direccion donde se va guardar y el nombre del archivo csv que obtengamos. 
    """

    hoy = date.today()
    meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
    dia = hoy.day
    mes = hoy.month
    anio = hoy.year
    return   (f'{datos}/{anio}-{meses[mes-1]}', f'/{datos}-{dia}-{mes}-{anio}')


def PrepararURL(url):
    """
    Prepara el url para poder hacer web scraping sin la limitacion de 100 filas de google sheets
    """

    ultimo_slash = url.rfind("/")
    anteultimo_slash = url.rfind("/", 0, ultimo_slash)

    recorte_url = url[anteultimo_slash +1: ultimo_slash]

    return "https://spreadsheets.google.com/tq?tqx=out:html&tq=&key=" + recorte_url

def run():
    """
    Es el cuerpo del programa
    """
    urls = [config('URL_MUSEOS'),
            config('URL_CINES'),
            config('URL_BIBLIOTECAS')]
    ObtenerCSV(urls)


if __name__ == "__main__":
    run()