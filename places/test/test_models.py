from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from dataleufu.models import UserProfile
from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from places.models import Category

class PlaceTests(APITestCase):

    def login(self):

        url = '/rest-auth/registration/'
        data = {'username': 'testuser', 'email': 'ma@xx.com.ar', 'password1': '1', 'password2': '1'}
        response = self.client.post(url, data, format='json')

        #Login
        url = '/rest-auth/login/'
        data = {'username': 'testuser',  'password': '1'}
        response = self.client.post(url, data, format='json')

        print "Respuesta //rest-auth/login/", response.data
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data.get('key'))






    def test_create_place_without_login(self):
        url = '/api_places/'
        data = {"category": {"pk": 1}, "description": "hola", "point": "SRID=4326;POINT(1 1)", "images": []}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_place(self):
        category = Category.objects.create(name="test")

        self.login()
        url = '/api_places/'
        data = {"category": {"pk": category.pk}, "description": "hola", "point": "SRID=4326;POINT(1 1)", "images": []}
        response = self.client.post(url, data, format='json')

        print "Respuesta /api_places/", response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
