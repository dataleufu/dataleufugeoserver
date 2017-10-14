# vim: set fileencoding=utf-8 :
from django.contrib.auth.models import User
from models import UserProfile, UserGroup
from rest_framework import serializers
from rest_framework import validators
from drf_extra_fields.fields import Base64ImageField
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
import base64


class CaseInsensitiveUniqueField(validators.UniqueValidator):
    def filter_queryset(self, value, queryset):
        """
        Filter the queryset to all instances matching the given attribute.
        """
        filter_kwargs = {self.field_name + '__iexact': value}
        return queryset.filter(**filter_kwargs)


class UserGroupSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = UserGroup
        fields = ('pk', "name", "description", "image")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True,
       validators=[validators.UniqueValidator(User.objects.all(),
       message="Ya existe otro usuario con ese nombre")])
    username = serializers.CharField(validators=[RegexValidator(regex=r'^[a-zA-Z][A-Za-z0-9_.]{0,19}$',
        message=(u'Solo se aceptan nombres '
                u'de usuarios con letras, números '
                u'y un máximo de 20 caracteres')),
        CaseInsensitiveUniqueField(User.objects.all(),
            message="Ya existe otro usuario con ese email")])

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'password')
        extra_kwargs = {'username': {'required': True},
                        'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], email=validated_data['email'],
            password=validated_data['password'])
        user_profile = UserProfile.objects.create(user=user)
        return user


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id', 'first_name', 'last_name', 'email', 'is_staff')


class UserProfileSerializer(serializers.ModelSerializer):
    user = FullUserSerializer()
    group = UserGroupSerializer()
    image = Base64ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('user', 'description', 'group', 'image')

