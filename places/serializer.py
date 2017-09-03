from models import Place, Category, Layer
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('pk', "name")

class PlaceSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Place
        fields = ('pk', "description", "title", "created", "image", "point", "category" )

class LayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Layer
        fields = ('pk', "name", "type", "category", "url", "color", "size", "visible")
