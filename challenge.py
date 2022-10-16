from hashlib import new
from bs4 import BeautifulSoup
import csv
import requests
from decouple import config
import os
from datetime import date
import pandas as pd
import numpy as np

def obtener_csv(urls):
    """
    Crea los archivos csv extrayendolos de google sheet y devuelve la ubicacion de los archivos.
    """
    ubicacion_archivos = []

    urls = list(map(preparar_url, urls))
    
    for i, url in enumerate(urls):
        if i == 0:
            tipos_datos = "museos"
        elif i == 1:
            tipos_datos = "cines"
        else:
            tipos_datos = "bibliotecas"
        
        direccion = obtener_direccion(tipos_datos)
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

def obtener_direccion(datos):
    """
    Genera la direccion donde se va guardar y el nombre del archivo csv que obtengamos. 
    """

    hoy = date.today()
    meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
    dia = hoy.day
    mes = hoy.month
    anio = hoy.year
    return   (f'{datos}/{anio}-{meses[mes-1]}', f'/{datos}-{dia}-{mes}-{anio}')


def preparar_url(url):
    """
    Prepara el url para poder hacer web scraping sin la limitacion de 100 filas de google sheets
    """

    ultimo_slash = url.rfind("/")
    anteultimo_slash = url.rfind("/", 0, ultimo_slash)

    recorte_url = url[anteultimo_slash +1: ultimo_slash]

    return "https://spreadsheets.google.com/tq?tqx=out:html&tq=&key=" + recorte_url

def crear_dfs(ubicaciones):
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

def normalizar_dfs(dataframes):
    """
    Normaliza los dataframes sacando espacios en blanco y remplazandolos por NaN.
    """
    for key in list(dataframes.keys()):
        dataframes[key].replace(['\xa0','','s/d',' '],np.nan, inplace=True)
        dataframes[key].drop_duplicates(inplace=True)

        if key == 'cines':
            dataframes[key]['espacio_INCAA'] = list(map(lambda x: x.lower() if isinstance(x, str) else x, dataframes[key]['espacio_INCAA']))
            dataframes[key].replace({np.nan:0,"si":1, "0":0}, inplace=True)

def unir_dfs(dataframes):
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

def obtener_cant_indices(df_unido, dataframes):
    """
    Genera un dataframe con la cantidad de indices por categoria, por fuente y por provincia y categoria.
    """

    dfs_to_concat = []
    
    aux = df_unido['categoría'].value_counts() 
    aux = aux.to_frame().reset_index()
    aux.rename(columns={'index':'categoria', 'categoría':'cant_registros'}, inplace=True)
    aux['categoria'] = list(map(lambda x: 'Categoria ' + x, aux['categoria']))
    dfs_to_concat.append(aux)


    aux = {}
    for dato in dataframes.keys():
        aux["Fuente " + dato] = dataframes[dato].shape[0]

    aux = pd.Series(aux).to_frame().reset_index()
    aux.rename(columns={'index':'categoria', 0:'cant_registros'}, inplace=True)
    dfs_to_concat.append(aux)


    aux = df_unido.value_counts(['provincia','categoría'], sort=False).to_frame().reset_index()
    aux['categoría'] = aux['provincia'].str.cat(aux['categoría'], sep=', ')
    aux.drop('provincia', axis=1, inplace=True)
    aux.rename(columns={0:'cant_registros','categoría':'categoria'}, inplace=True)
    dfs_to_concat.append(aux)

    return pd.concat(dfs_to_concat, ignore_index=True)

def obtener_info_cines(cines):
    """
    Devuelve un dataframe con la cantidad de panttallas, butacas y espacios INCAA por provincia.
    """

    return cines[['Provincia','Pantallas', 'Butacas', 'espacio_INCAA']].groupby('Provincia').sum().reset_index()


def run():
    """
    Es el cuerpo del programa
    """

    urls = [config('URL_MUSEOS'),
            config('URL_CINES'),
            config('URL_BIBLIOTECAS')]
    ubicaciones = obtener_csv(urls)
    dataframes = crear_dfs(ubicaciones)
    normalizar_dfs(dataframes)
    df_unido = unir_dfs(dataframes)
    df_cant_indices = obtener_cant_indices(df_unido, dataframes)
    df_info_cines = obtener_info_cines(dataframes['cines'])
    

    print(df_info_cines)



if __name__ == "__main__":
    run()