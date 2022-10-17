from decouple import config
from sqlalchemy import create_engine, text

def runQuery(engine, query):
    engine.connect().execute((text(query)))
    #engine.execute(query)

def run():
    """
    Cuerpo del programa.
    """

    hostname = config('HOSTNAME')
    database = config('DATABASE')
    username = config('USERNAME')
    passw = config('PASSWORD')
    port = config('PORT_ID')

    engine = create_engine(f'postgresql://{username}:{passw}@{hostname}:{port}/{database}') # Error fatal: no existe la base de datos "db_alkemy"

    query = ""
    with open("crear_tabla_museos_cines_biblio.sql", "r", encoding='utf8') as archivo:
        for linea in archivo:
            query += linea
  
    runQuery(engine, query)

if __name__ == '__main__':
    run()