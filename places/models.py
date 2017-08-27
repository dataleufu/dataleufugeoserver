# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.gis.db import models

class Place(models.Model):

    point = models.PointField()
    title = models.CharField(max_length=100, blank=True, verbose_name=u'título')
    description = models.CharField(max_length=3000, verbose_name=u'descripción',
                                   help_text=u'máximo 3000 caracteres')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'fecha de creación')
    image = models.ImageField(blank=True)

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.description