# Servidor de las capas del proyecto Dataleufu.

Para levantar el proyecto desde cero se siguen los pasos del tutorial de GeoDjango.

python manage.py makemigrations
python manage.py sqlmigrate places 0001
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
