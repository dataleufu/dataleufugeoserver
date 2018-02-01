# Servidor de las capas del proyecto Dataleufú

Dataleufú es un Mapeo ambiental ciudadano del Río Negro, Limay y Neuquén que busca visibilizar nuestros conflictos y amenazas ambientales, para convertirlas en desafíos colectivos que movilicen a la ciudadanía para trabajar conjuntamente en sus soluciones.

Este proyecto es el servidor de datos de las entidades y los datos geográficos.

Es recomendable leer la documentación de [GeoDjango](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/) para ver cada paso en detalle.

##Prerequisitos

Python >= 2.7
pip
virtualenv

##Instalación

Una vez instalados los prerequisitos, crear un entorno virtual con virtualenv

```
cd dataleufugeoserver
virtualenv .
```

Activar el entorno virtual

```
source bin/activate
```

Instalar las dependencias

```
pip install -r requirements.txt
```

Instalar  djangorestframework-gis por separado

```
pip install --no-use-wheel djangorestframework-gis
```

Para no tener en el repositorio la configuración del entorno de desarrollo o producción, settings.py import local_settings.py.
Copiar el local_settings de ejemplo, modificarlo con los parámetros de conexión a la base y renombrarlo a localsettings.py.


```
cp dataleufu/local_settings.py.sample dataleufu/local_settings.py
```

##Base de datos

Actualmente el proyecto está usan sqllite con la extensión geográfica.


Inicializar la base de datos

```
python manage.py migrate
```

Crear un usuario
```
python manage.py createsuperuser
```


El proyecto ya está listo para ejecutarse

```
python manage.py runserver
```

Dentro del admin crear categorías y capas para visualizar en el mapa.


1. Creo el usuario
curl -X POST -d "username=pepe33&password1=maradona&password2=maradona&email=pepe33@pepe.com" http://localhost:8000/rest-auth/registration/

{"key":"40c9492733330efeb383bb3fc22ab369c3054b81"}

2. Login
curl -X POST -d "username=pepe&password=maradona"  http://localhost:8000/rest-auth/login/

{"key":"40c9492733330efeb383bb3fc22ab369c3054b81"}

3. Obtener usuario
curl -X GET -d "username=pepe"  http://localhost:8000/rest-auth/user/ -H "Authorization: Token 40c9492733330efeb383bb3fc22ab369c3054b81"

{"pk":14,"username":"pepe","email":"pepe@pepe.com","first_name":"","last_name":""}

4. Logout
curl -X POST  http://localhost:8000/rest-auth/logout/

5. Reset contraseña
curl -X POST -d "email=pepe@pepe.com"  http://localhost:8000/rest-auth/password/reset/

No funciona

6. Cambiar contraseña
curl -X POST -d "new_password1=mariposa&new_password2=mariposa&old_password=maradona"  http://localhost:8000/rest-auth/password/change/ -H "Authorization: Token 40c9492733330efeb383bb3fc22ab369c3054b81"

{"detail":"New password has been saved."}

curl -X POST -d "new_password1=mariposa&new_password2=mariposaxx&old_password=mariposax"  http://localhost:8000/rest-auth/password/change/ -H "Authorization: Token 40c9492733330efeb383bb3fc22ab369c3054b81"
{"new_password2":["The two password fields didn't match."]}

7. Auth en Facebook


curl -X POST -d "aZCXKZCI5VmpC6M8ePGTZAmVtDWrFuZAGmZCCPsvdi32LFZCTHweNISzz4jhvcwhLaNfIemHX7m4kvgZCS7OkVN1PFfGvn8nTpqUNTMsdtiYmmrileL7Wx0MhNSHF4fddpZAYZBTPHhp4GtkDS8IPr62aNpQXfJ8gmKmMxgC4AAZDZD"  http://localhost:8000/rest-auth/facebook/
{"key":"543f7833cefcf8e4d1297f16de1b4e0290790c27"}

curl -X POST -d "access_token=EAAbq3BT07awBAFNNgNfrnA2J5AdznZAW3WuBcPnw1iZCXZCYnnSSBCppTCwPKXGT4aakwmbu1DhvUOlphl8Jm1yjjbJmrZBNUZBwb1ZBq1ADTWzx9UaEbFZBPNnwsZCNuw87EQIzni3Qlb6BTvhCuYhLVxolZBk122Ktqgqk4wJDjuCQ7jLNFZCMZCUsY14lM3ODfu8ZB9wZC2kBtqAZDZD"  http://localhost:8000/rest-auth/facebook/



Token inválido:
curl -X POST -d "aZCXKZCI5VmpC6M8ePGTZAmVtDWrFuZAGmZCCPsvdi32LFZCTHweNISzz4jhvcwhLaNfIemHX7m4kvgZCS7OkVN1PFfGvn8nTpqUNTMsdtiYmmrileL7Wx0MhNSHF4fddpZAYZBTPHhp4GtkDS8IPr62aNpQXfJ8gmKmMxgC4AAZDZDss"  http://localhost:8000/rest-auth/facebook/

{"non_field_errors":["Incorrect value"]}

8. Crear un punto (con ek key que devolvió la autorización de Facebook)

curl -X POST -d "description=test&category=1&point=POINT(-71.060316 48.432044)" http://localhost:8000/api_places/ -H "Authorization: Token 543f7833cefcf8e4d1297f16de1b4e0290790c27"


Circuito
========

Registro común:

A. Ingreso por primera vez
1. El usuario se registra.
2. El usuario se loguea  y guarda el token. En el test vi que el registro ya devuelve el token.
3. Se pide su profile.

B. Tiene registro
1. El usuario se loguea  y guarda el token.
2. Se pide su profile.

Registro con Facebook

A. No está logueado
1. El usuario se loguea en Facebook
2. Se pide el auth de FAcebook.
3. Se guarda el token
4. Se pide su profile.

B. Inicio estando logueado a Facebook
1. Se pide el auth de FAcebook.
2. Se guarda el token
3. Se pide su profile.

Para ver:
Facebook no devuelve el mail, por eso ya no es clave para registrarse.
En registro manual, pedir el mail y verificar a mano que sea único.
Perfil: crearlo en el save de User para que todos lo tengan.
Facebook no crea un username, hay que armarlo a mano.
