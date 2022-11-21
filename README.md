
# App Flask

Proyecto de practica de CRUD 


## Authors

- [@Raisa320](https://github.com/Raisa320)


## Environment Variables

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env

`SECRET_KEY`

`FLASK_DEBUG`

`FLASK_APP=run.py`

`SQLALCHEMY_DATABASE_URI`

`SQLALCHEMY_TRACK_MODIFICATIONS`

## Installation

Para poder ejecutar el proyecto debe
- Crear un entorno virtual de python
```bash
  virtualenv env
```
- Instalar los requirimientos
```bash
  pip install -r .\requirements.txt
```    
- Iniciar las migraciones y construir la bd
```bash
  flask db init
``` 
```bash
  flask db migrate -m "primera migrate"
``` 
```bash
  flask db upgrade
``` 
- Insertar los Roles en la tabla Roles
    
Primero ingresar a la shell de flask

```bash
  flask shell
```    
Luego ejecutar 
```bash
 Role.insert_roles()
 exit()
```
    
## Usage
```bash
flask run 
or
py run.py
```
- Utilizar la implementación JSON que envia posteos

Primero levantar el app

```bash
flask run 
or
py run.py
```

Luego en otra terminal del (env) hacer la peticion: (reemplazar  example@gmail.com:123456 con un correo y contraseña existente en tu base de datos)

```bash
http --auth example@gmail.com:123456 --json POST http://127.0.0.1:5000/post/postJson/ "body=post1"
```
