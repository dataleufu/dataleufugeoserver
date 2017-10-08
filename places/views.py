# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.serializers import serialize
from models import Place, Category, Layer
from serializer import PlaceSerializer, CategorySerializer, LayerSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import permissions


class GeoPlaceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Place
        geo_field = 'point'
        fields = ('description', 'id', 'category')


class PlacesPagination(GeoJsonPagination):
    page_size = 10000


class PlacesListAPIView(generics.ListAPIView):
    serializer_class = GeoPlaceSerializer
    pagination_class = PlacesPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        category_pk = self.kwargs['category_pk']
        return Place.objects.filter(category__pk=category_pk)


class PlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class LayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
