# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.serializers import serialize
from models import Place

from rest_framework import viewsets
from serializer import PlaceSerializer


def place_view(request):
    points_as_geojson = serialize('geojson', Place.objects.all(), fields=('description', 'pk'), geometry_field='point',)
    response = HttpResponse(points_as_geojson, content_type='json')
    return response

class PlaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
