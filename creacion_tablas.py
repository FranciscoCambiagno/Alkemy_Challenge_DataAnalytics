from ctypes import cast
from curses import A_ALTCHARSET
from re import A
from decouple import config
import sqlalchemy
from sqlalchemy import create_engine, text

def run_query(engine, query):   
    """
    Ejecuta la query obtenida de los archivos .sql en la base de datos.
    """

    engine.connect().execute((text(query)))
         

def leer_sql(nombre):
    """
    Obtiene la query para crear las tablas de los archivos .sql. 
    """

    query = ""
    with open(nombre + ".sql", "r", encoding='utf8') as archivo:
        for linea in archivo:
            query += linea
    
       

    return query

def run():
    """
    Cuerpo del programa.
    """

    hostname = config('HOSTNAME')
    database = config('DATABASE')
    username = config('USERNAME')
    passw = config('PASSWORD')
    port = config('PORT_ID')

    nombres_archivos_sql = ['crear_tabla_cant_indices', 'crear_tabla_cines', 'crear_tabla_museos_cines_biblio']

    engine = create_engine(f'postgresql://{username}:{passw}@{hostname}:{port}/{database}') 
    try:

        for nombre in nombres_archivos_sql:
            try:

                query = leer_sql(nombre)

            except FileNotFoundError:
                print(f'No se encontro el archivo {nombre}.sql')
                continue

            try:

                run_query(engine, query)

            except sqlalchemy.exc.ProgrammingError:
                print(f'La {nombre[6:-1]} ya esta creada.')            
    
    except sqlalchemy.exc.OperationalError:
            print("Hay un error con los datos de conexion a la base de datos.")
    

if __name__ == '__main__':
    run()
