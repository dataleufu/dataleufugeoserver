# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.serializers import serialize
from models import UserProfile, UserGroup
from serializer import UserProfileSerializer, UserGroupSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import update_last_login
from allauth.socialaccount import providers
from allauth.socialaccount.helpers import complete_social_login, complete_social_signup
from allauth.socialaccount.forms import SignupForm
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.account.forms import ResetPasswordForm

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = ()

class UserGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        if 'token' in request.data:
            token = get_object_or_404(Token, key=request.data['token'])
            user = token.user
        else:

            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
        user_profile = UserProfile.objects.get(user_id=user.id)
        user_profile = UserProfileSerializer().to_representation(user_profile)
        user_profile = UserProfileSerializer(user.profile).data

        update_last_login(None, user)
        return Response({'token': token.key,
                         'user_profile': user_profile})

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_user = serializer.instance
        user_signed_up.send(sender=self.__class__, request=request, user=new_user)

        # Creo un token para el nuevo usuario
        token, created = Token.objects.get_or_create(user=new_user)
        headers = self.get_success_headers(serializer.data)

        # Y lo agrego a la respuesta que se le envía
        request_data = request.data
        request_data['token'] = token.key
        request_data['user_profile'] = UserProfileSerializer(new_user.profile).data
        return Response(request_data, status=status.HTTP_201_CREATED, headers=headers)

class SocialAccountView(APIView):
    permission_classes = ()

    def get_provider(self):
        return providers.registry.by_id(self.provider_id)

    def get_user_response(self, user):
        """ Returns a response with some fields set with user information """
        token, _ = Token.objects.get_or_create(user=user)
        user_profile = UserProfileSerializer(user.profile).data
        update_last_login(None, user)
        return Response({'token': token.key,
                         'is_staff': user.is_staff,  # Redundancia por Backward-compatibility
                         'user_profile': user_profile})

class FacebookLoginView(SocialAccountView):
    provider_id = 'facebook'

    def get_sociallogin(self, request):
        app = SocialApp.objects.get(provider='facebook')
        fb_auth_token = SocialToken(app=app, token=request.data['access_token'])
        login = fb_complete_login(request, app, fb_auth_token)
        login.token = fb_auth_token
        login.state = SocialLogin.state_from_request(request)
        return login

    def post(self, request):
        login = self.get_sociallogin(request)
        complete_social_login(request, login)
        if not login.is_existing:
            # No tiene usuario, se tiene que registrar
            request.session.save()
            return Response({'session_key': request.session.session_key})
        else:
            # Tiene usuario, se logueo correctamente
            return self.get_user_response(login.user)

class ResetPasswordView(APIView):
    permission_classes = ()

    def post(self, request):
        reset_form = ResetPasswordForm(data=request.data)
        if not reset_form.is_valid():
            raise ValidationError(reset_form.errors)
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        reset_form.save(**opts)
        return Response({})

class ResetPasswordView(APIView):
    permission_classes = ()

    def post(self, request):
        reset_form = ResetPasswordForm(data=request.data)
        if not reset_form.is_valid():
            raise ValidationError(reset_form.errors)
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        reset_form.save(**opts)
        return Response({})

class SocialAccountSignupView(SocialAccountView):
    def validate_request(self, request):
        if 'session_key' not in request.data:
            raise ValidationError('No session key provided')

    def set_session(self, request):
        from django.utils.importlib import import_module
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.data['session_key']
        request.session = engine.SessionStore(session_key)

    def get_session_data(self, request):
        data = request.session.get('socialaccount_sociallogin')
        if not data:
            raise ValidationError('This user has no session on the server')
        return data

    def get_sociallogin(self, request, data):
        login = SocialLogin.deserialize(data)
        login.state = SocialLogin.state_from_request(request)
        return login

    def post(self, request):
        """ Data expected:
            {
              username: name,
              email: string(valid email),
              session_key: string(key obtained with a post to TwitterLoginView)
            }
        """
        self.validate_request(request)

        # Obtengo el session_id
        self.set_session(request)

        # Chequeo que tenga una sesión en el servidor
        data = self.get_session_data(request)

        # Valido los campos de signup (username y email)
        login = self.get_sociallogin(request, data)
        form = SignupForm(data=request.data, sociallogin=login)
        if not form.is_valid():
            raise ValidationError(form.errors)

        # Guardo el usuario y creo su binding con la cuenta social
        new_user = form.save(request)
        complete_social_signup(request, login)
        return self.get_user_response(new_user)

class FacebookSignupView(SocialAccountSignupView):
    provider_id = 'facebook'

    def get_sociallogin(self, request, data):
        app = SocialApp.objects.get(provider='facebook')
        fb_auth_token = SocialToken(app=app, token=data['token']['token'])
        login = fb_complete_login(request, app, fb_auth_token)
        login.token = fb_auth_token
        login.state = SocialLogin.state_from_request(request)
        return login
