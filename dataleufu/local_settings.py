# vim: set fileencoding=utf-8 :
import os

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y^rl=f&c_*=j9w4tw7ow_(%205=#cat46h5fdtvvd(mpt59t*r'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'dataleufu.sqlite3'),
    }
}

ALLOWED_HOSTS = ['mexico.q123.com.ar',  'localhost']

CORS_ORIGIN_WHITELIST = (
        'localhost:3002',
        'hostname.example.com',
        'http://localhost:3002'
    )
