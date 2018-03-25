# -*- coding: iso-8859-1 -*-
from models import Place, Category, Layer, PlaceImage
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.core.files.base import ContentFile
import base64
from dataleufu.serializer import UserProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
from easy_thumbnails.files import get_thumbnailer
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('pk', "name")


class RelatedCategorySerializer(serializers.RelatedField):
    """Para poder serializar la categoría completa es necesario definir este serializar derivando de RelatedField"""

    class Meta:
        model = Category
        fields = ('pk', "name")

    def to_representation(self, obj):
        return {
            'pk': obj.pk,
            'name': obj.name
        }

    def to_internal_value(self, data):
        #TODO revisar por qué se recibe id y no pk
        return Category.objects.get(pk=data.get('pk') or data.get('id'))


class PlaceImageSerializar(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    """Action no es parte del modelo, pero es el mecanismo para el ABM de imágenes"""
    action = serializers.CharField(read_only=True, required=False)
    pk = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = PlaceImage
        fields = ('pk', "image", "action" )


    def to_representation(self, obj):

        ret =  super(serializers.ModelSerializer, self).to_representation(obj)
        ret['image'] = serializers.URLField().to_representation(full_media_url(obj.get_image_url)),
        return ret

    def to_internal_value(self, data):
        #TODO revisar si es necesario
        ret = super(serializers.ModelSerializer, self).to_internal_value(data)
        ret.update({'action': data.get('action'), 'pk': data.get('pk')})
        ret.action = data.get('action')
        ret.pk = data.get('pk')
        return ret


class PlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializar(many=True, read_only=False)
    owner = UserProfileSerializer(required=False, read_only=True)
    category = RelatedCategorySerializer(queryset=Category.objects.all(), read_only=False )

    class Meta:
        model = Place
        fields = ('pk', "description", "created", "images", "point", "category", "owner" )

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        place = Place.objects.create(**validated_data)
        for image_data in images_data:
            PlaceImage.objects.create(place=place, image=image_data['image'])
        return place

    def update(self, instance, validated_data):
        updated = False
        if validated_data.get('description'):
            instance.description = validated_data.get('description', instance.description)
            updated = True
        if validated_data.get('category'):
            instance.category = validated_data.get('category', instance.category)
            updated = True
        images_data = validated_data.pop('images')
        for image_data in images_data:
            action = image_data['action']
            if action == 'delete':
                if image_data['pk']:
                    try:
                        image = PlaceImage.objects.get(pk=image_data['pk'])
                        image.delete()
                        updated = True
                    except ObjectDoesNotExist:
                        pass

            elif action == 'new':
                PlaceImage.objects.create(place=instance,  image=image_data['image'])
                updated = True
        if updated:
            instance.save()
        return instance


class LayerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)

    class Meta:
        model = Layer
        fields = ('pk', "name", "type", "category", "url", "color", "size", "visible")

def full_media_url(url):
    if url.startswith("//"):
        return "http:" + url
    elif url.startswith("http"):
        return url
    else:
        return settings.ADMIN_URL + url
