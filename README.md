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
