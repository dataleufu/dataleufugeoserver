# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.gis import admin
from .models import Place, Category, Layer

class LayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'color', 'size', 'visible')
    ordering = ('name', )
    list_filter = ('category', )


class PlaceAdmin(admin.ModelAdmin):

    list_display = ('short_description', 'category', 'created', 'point')
    ordering = ('created', )
    list_filter = ('category', )

admin.site.register(Place, PlaceAdmin)
admin.site.register(Category, admin.GeoModelAdmin)
admin.site.register(Layer, LayerAdmin)
