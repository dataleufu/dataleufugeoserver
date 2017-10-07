from models import Place, Category, Layer, PlaceImage
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.core.files.base import ContentFile
import base64


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('pk', "name")


class PlaceImageSerializar(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = PlaceImage
        fields = ('pk', "image" )


class PlaceSerializer(serializers.ModelSerializer):
    images = PlaceImageSerializar(many=True, read_only=False)

    class Meta:
        model = Place
        fields = ('pk', "description", "title", "created", "images", "point", "category" )

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        place = Place.objects.create(**validated_data)
        for image_data in images_data:
            PlaceImage.objects.create(place=place, **image_data)
        return place


class LayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Layer
        fields = ('pk', "name", "type", "category", "url", "color", "size", "visible")
