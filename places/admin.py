# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.gis import admin
from .models import Place, Category, Layer

admin.site.register(Place, admin.GeoModelAdmin)
admin.site.register(Category, admin.GeoModelAdmin)
admin.site.register(Layer, admin.GeoModelAdmin)
