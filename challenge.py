from hashlib import new
from bs4 import BeautifulSoup
import csv
import requests
from decouple import config
import os
from datetime import date
import pandas as pd
import numpy as np

def ObtenerCSV(urls):
    """
    Crea los archivos csv extrayendolos de google sheet y devuelve la ubicacion de los archivos.
    """
    ubicacion_archivos = []

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

        ubicacion_archivos.append(direccion[0] + direccion[1] + ".csv")

        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        tables = soup.find_all("table")
        for table in tables:
            with open(direccion[0] + direccion[1] + ".csv", "w", encoding='utf8') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
                wr.writerows([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])
    
    return ubicacion_archivos

def obtenerDireccion(datos):
    """
    Genera la direccion donde se va guardar y el nombre del archivo csv que obtengamos. 
    """

    hoy = date.today()
    meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
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

def CrearDFs(ubicaciones):
    """
    Devuelve un diccionario con los dataframes de museos, cines y bibliotecas.
    """
    
    dataframe = {}

    for i, ubicacion in enumerate(ubicaciones):
        if i == 0:
            tipos_datos = "museos"
        elif i == 1:
            tipos_datos = "cines"
        else:
            tipos_datos = "bibliotecas"

        dataframe[tipos_datos] = pd.read_csv(ubicacion)

    return dataframe

def NormalizarDFs(dataframes):
    """
    Normaliza los dataframes sacando espacios en blanco y remplazandolos por NaN.
    """
    for key in list(dataframes.keys()):
        dataframes[key].replace(['\xa0','','s/d',' '],np.nan, inplace=True)
        dataframes[key].drop_duplicates(inplace=True)

def UnirDFs(dataframes):
    """
    Une los data frames en uno solo con que solo contiene las columnas cod_localidad, id_provincia, id_departamento, categoría, provincia, localidad, nombre, domicilio, código postal, número de teléfono, mail, web.
    """

    columns_to_delete = [['Observaciones', 'subcategoria','piso', 'cod_area', 'Latitud', 'Longitud', 'TipoLatitudLongitud', 'Info_adicional', 'fuente', 'jurisdiccion', 'año_inauguracion', 'actualizacion'],                           # museos
                        ['Observaciones','Departamento','Piso','cod_area','Información adicional','Latitud', 'Longitud', 'TipoLatitudLongitud','Fuente', 'tipo_gestion','Pantallas', 'Butacas', 'espacio_INCAA','año_actualizacion'],   # cines
                        ['Observacion', 'Subcategoria', 'Departamento', 'Piso', 'Cod_tel', 'Información adicional', 'Latitud', 'Longitud', 'TipoLatitudLongitud', 'Fuente', 'Tipo_gestion', 'año_inicio', 'Año_actualizacion']]         # bibliotecas

    new_names = ["cod_localidad", "id_provincia", "id_departamento", "categoría", "provincia", "localidad", "nombre", "domicilio", "código postal", "número de teléfono", "mail", "web"]
    
    auxs_dfs = []

    for to_delete, df in zip(columns_to_delete, dataframes.values()):

        df_aux = df.drop(labels=to_delete, axis=1)
        df_aux.rename(columns=dict(zip(list(df_aux.columns), new_names)), inplace=True)
        auxs_dfs.append(df_aux)

    return pd.concat(auxs_dfs, ignore_index=True)

def run():
    """
    Es el cuerpo del programa
    """

    urls = [config('URL_MUSEOS'),
            config('URL_CINES'),
            config('URL_BIBLIOTECAS')]
    ubicaciones = ObtenerCSV(urls)
    dataframes = CrearDFs(ubicaciones)
    NormalizarDFs(dataframes)
    df_unido = UnirDFs(dataframes)
    

    print(df_unido.head(5))
    print(df_unido.tail(5))


    



if __name__ == "__main__":
    run()