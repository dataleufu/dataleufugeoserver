# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class UserGroup(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default="", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u'Grupo/Adherente'
        verbose_name_plural = u'Grupos/Adherentes'


class UserProfile(models.Model):

    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default="", blank=True, null=True)
    group = models.ForeignKey(UserGroup, null=True, blank=True)

    class Meta:
        verbose_name = u'perfil'
        verbose_name_plural = u'perfiles'

    def __unicode__(self):
        return u'Perfil de {0.user}'.format(self)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
