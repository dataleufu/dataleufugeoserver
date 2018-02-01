from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from dataleufu.models import UserProfile
from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class AccountTests(APITestCase):
    def test_create_account(self):
        url = '/rest-auth/registration/'
        data = {'username': 'DabApps', 'email': 'ma@xx.com.ar', 'password1': '1', 'password2': '1'}
        response = self.client.post(url, data, format='json')

        print "Respuesta /rest-auth/registration/", response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Verifico respuesta y modelo
        self.assertEqual(User.objects.all()[0].pk, response.data.get('user'))

        #Devuelve el user_profile
        self.assertEqual(User.objects.all()[0].email, response.data.get('user_profile')['user']['email'], 'ma@xx.com.ar')

        #Verifico el modelo
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'DabApps')
        #En el registro se crea el profile
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().user.username, 'DabApps')


        #Login
        url = '/rest-auth/login/'
        data = {'username': 'DabApps',  'password': '1'}
        response = self.client.post(url, data, format='json')
        print "Respuesta /rest-auth/login/", response.data

        self.assertTrue(self.client.login(username='DabApps', password='1'))
        token = Token.objects.get(user__username='DabApps')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)



    def test_profile(self):
        url = '/rest-auth/registration/'
        data = {'username': 'DabApps', 'email': 'ma@xx.com.ar', 'password1': '1', 'password2': '1'}
        response = self.client.post(url, data, format='json')

        print "Respuesta /rest-auth/registration/", response

        #En el registro se crea el profile
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().user.username, 'DabApps')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data.get('key'))

        url = '/rest-auth/user/'
        data = {'username': 'DabApps'}
        response = self.client.get(url, data, format='json')
        print "Respuesta /rest-auth/user/", response

        url = '/api_user_profile/%s/' % response.data.get('pk')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.data.get('user')["username"], 'DabApps' )

        print "Respuesta api_user_profile", response

    def test_facebook_auth(self):
        s = SocialApp.objects.create(provider='facebook', name='facebook', client_id='1947080825564588', secret='bf74bdc2f7063c1884ab02e6a895b07d')
        s.sites = [Site.objects.all()[0]]
        s.save()

        url = '/rest-auth/facebook/'
        #Token de un usuario de prueba creado en Facebook
        data = {'access_token': 'EAAbq3BT07awBAGDZBCZBZAXR21R15SZCUGEJ44scMs3rkJZAueLvtYpHl0wM8s5ZAuywazIeR2FpYfLi3ekH6VKgqK4AEJehapjyOyD39ZAT73hASlm3ZASZCagC6FbNzhDT4NAjm7sxnbbItGo00A8HbWWbhkMQ5ZBr67NZCtt8nP5VQbiW83uj6zkjq25CH2voi52rZANmZB36P17SBlZAWXaNS7Y5RdHsqRXTZCdD75DLn81PQZDZD'}

        response = self.client.post(url, data, format='json')
        print "Respuesta test_facebook_auth", response

        #En el registro se crea el profile
        self.assertEqual(UserProfile.objects.count(), 1)

        #Se crea un usuario
        self.assertEqual(UserProfile.objects.all()[0].pk, response.data.get('user'))
