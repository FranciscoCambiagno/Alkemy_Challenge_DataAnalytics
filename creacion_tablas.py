from decouple import config
from sqlalchemy import create_engine, text

def run_query(engine, query):
    engine.connect().execute((text(query)))

def leer_sql(nombre):
    query = ""
    with open(nombre, "r", encoding='utf8') as archivo:
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

    nombres_archivos_sql = ['crear_tabla_cant_indices.sql','crear_tabla_cines.sql','crear_tabla_museos_cines_biblio.sql']

    engine = create_engine(f'postgresql://{username}:{passw}@{hostname}:{port}/{database}') 

    for nombre in nombres_archivos_sql:
        query = leer_sql(nombre)
    
        run_query(engine, query)

if __name__ == '__main__':
    run()