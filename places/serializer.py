from models import Place
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

class PlaceSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    class Meta:
        model = Place
        fields = ('pk', "description", "title", "created", "image", "point" )

