# Alkemy_Challenge_DataAnalytics
Proyecto realizado para el Alkemy Challenge, para la aceleracion en Data Analytics + Python.

### Deploy
------
Una vez que hayamos clonado el repositorio, debemos crear un entorno virtual en la misma carpeta del repositorio. Eso la hacemos con el siguiente comando
```
python -m venv venv
```
Una vez que este creado el entorno virtual tenemso que activarlo para empezar a usarlo. Parado en el mismo directorio donde lo creamos debemos escribir lo siguiente:
En linux
```
. venv/bin/activate
```
Y en windows
```
./venv/Scripts/activate
```
A continuacion debemos instalar las librerias necesarias que esta indicadas por el archivo `requirements.txt`
```
pip install -r requirements.txt
```
Despues debemos instalar PostgreSQL con estos comandos en el caso de linux:
```
sudo apt update

sudo apt install postgresql postgresql-contrib
```
Una vez instalado debemos entrar desde la terminal con
```
sudo su - postgres
```
Despues debemos escribir el siguiente comadno apra poder empezar a crear nuestro usuario y la base de datos:
```
psql
```
Creacion deusuario y contraseña:
```
CREATE USER fran WITH PASSWORD 'Alkemy2022';
```
Aca puede poner el nombre de usuario y contraseñe que desee. Para eso solo hay que cambiar donde dice `fran` en el comando de arriba, para cambiar el usuario y donde dice `'Alkemy2022'` para cambiar la contraseña.

Para crear la base de datos usamos:
```
CREATE DATABASE db_alkemy WITH OWNER fran;
```
Aca podemos cambiar le nombre de la base de datos y recuerde cambiar el nombre del owner por el nombre de usario que haya elegido anteriormente.

Una vez hecho estos pasos, debemos ir al archivo `.env` y cambiar el nombre de usario en `USERNAME`, la contraseña en `PASSWORD` y el nombre de la base de datos en `DATABASE`, por lo que hayamos puesto anteriormente (Si es que los cambaimos).

Ahora si, podemos empezar a ejecutar todo empezando primero por `creacion_tablas.py` y despues por `challenge.py`.
