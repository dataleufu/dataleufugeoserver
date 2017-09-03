# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Place(models.Model):

    point = models.PointField()
    title = models.CharField(max_length=100, verbose_name=u'título')
    description = models.CharField(max_length=3000, verbose_name=u'descripción',
                                   help_text=u'máximo 3000 caracteres')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'fecha de creación')
    image = models.ImageField()
    category = models.ForeignKey(Category, verbose_name=u'categoría',
                              related_name=u'places')

    def __str__(self):
        return self.description


class Layer(models.Model):

    TYPES = (
        (1, "Interna"),
        (2, "Externa"),
    )

    name = models.CharField(max_length=100, verbose_name=u'título')
    type = models.IntegerField(choices=TYPES,
                                  default=TYPES[0], verbose_name=u'tipo de capa')
    category = models.ForeignKey(Category, verbose_name=u'categoría',
                              related_name=u'layers', blank=True)
    url = models.URLField(blank=True, verbose_name=u'Url de la nube de almacenamiento')
    color = models.CharField(max_length=20, verbose_name=u'color')
    size = models.IntegerField(verbose_name=u'tamaño en píxeles')
    visible = models.BooleanField(verbose_name=u'visible al inicio', default=True)




    def __str__(self):
        return self.name
